import json
import os
import shutil
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pc_org_bot import alert

def load_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'config.json')
    
    with open(config_path, 'r') as f:
        return json.load(f)

config = load_config()

class FileOrganizerHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            if filename.startswith(("New", "Nuevo")):
                return 
            self.process_file(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self.process_file(event.dest_path)

    def process_file(self, source_path):
        time.sleep(1)
        if not os.path.exists(source_path):
            return

        filename = os.path.basename(source_path)
        extension = os.path.splitext(filename)[1].lower()
        destination_dir = config['folders'].get(extension)
        
        if destination_dir:
            os.makedirs(destination_dir, exist_ok=True)
            date_folder = datetime.now().strftime("%Y-%m-%d")
            new_name = f"NOTE_{date_folder}_{filename}"
            destination = os.path.join(destination_dir, new_name)
            
            try:
                shutil.move(source_path, destination)
                alert(f"File organized: {filename}")
            except Exception:
                pass

watch_path = config['default_folder']
event_handler = FileOrganizerHandler()
observer = Observer()
observer.schedule(event_handler, watch_path, recursive=False)

observer.start()
print("Listening for changes...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()