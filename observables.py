
import multiprocessing
import time
from os.path import basename
from pathlib import Path

import rx
from rx import operators as ops
from rx.core.typing import Observable
from rx.scheduler import ThreadPoolScheduler
from rx.subject import Subject

thread_count = multiprocessing.cpu_count()
thread_pool_scheduler = ThreadPoolScheduler(thread_count)
print("Cpu count is : {0}".format(thread_count))


def get_date(x):
    return x.split("-")[1].replace(".tiff","")

async def process_ros(x,add_done_callback):
    print("CREATING ROS FILE", x)
    time.sleep(10)
    Path('./data/ros_'+x[0]+"-"+get_date(x[1])+".tiff").touch()

def create_pot_data(x):
    print("CREATING POT ROS DATA", x)
    time.sleep(1)
    return get_date(x[0])



source = Subject()

td = source.pipe(ops.filter(lambda text: text.find('td')>=0), ops.subscribe_on(thread_pool_scheduler))
temp = source.pipe(ops.filter(lambda text: text.find('temp')>=0), ops.subscribe_on(thread_pool_scheduler))
radar = source.pipe(ops.filter(lambda text: text.find('radar')>=0))

pot_ros = rx.combine_latest(temp, td).pipe( ops.filter(lambda values: get_date(values[0])==get_date(values[1])), ops.map(create_pot_data), ops.subscribe_on(thread_pool_scheduler))
# rx.combine_latest(pot_ros, radar).subscribe(process_ros, scheduler=thread_pool_scheduler)
rx.combine_latest(pot_ros, radar).pipe(ops.flat_map(lambda x: rx.from_future(process_ros))).subscribe(lambda x: print(x))


