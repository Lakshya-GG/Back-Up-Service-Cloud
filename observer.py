import json
import logging
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set up logging
logging.basicConfig(filename='./backups/file_events.log', level=logging.INFO,
                    format='%(message)s')

class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        self.log_event("modified", event)

    def on_created(self, event):
        self.log_event("created", event)

    def on_deleted(self, event):
        self.log_event("deleted", event)

    def on_moved(self, event):
        self.log_event("moved", event)

    def log_event(self, action, event):
        log_data = {
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "action": action,
            "event_name": event.event_type,
            "src_path": event.src_path,
            "is_directory":event.is_directory
        }
        if hasattr(event, 'dest_path'):
            log_data["dest_path"] = event.dest_path
        logging.info(json.dumps(log_data))

if __name__ == "__main__":
    # Define the directory to watch
    directory_to_watch = './myDir'

    # Create an event handler
    event_handler = FileHandler()

    # Create an observer for the directory
    observer = Observer()
    observer.schedule(event_handler, directory_to_watch, recursive=True)

    # Start the observer
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
