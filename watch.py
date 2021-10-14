import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from observables import source


class MyHandler(FileSystemEventHandler):
    def next_source(self, path):
        source.on_next(path)
    
    def on_created(self, event):
        self.next_source(event.src_path)
    
    def on_modified(self, event):
        self.next_source(event.src_path)
    
if __name__ == "__main__":
    path = './data'

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
