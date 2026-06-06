import json
import os
import logging
import shutil
import time
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from pc_org_bot import alert

logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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
    def is_file_ready(self, path):
        try:
            with open(path, 'rb'):
                return True
        except IOError:
            return False

    def on_moved(self, event):
        if not event.is_directory:
            self.process_file(event.dest_path)

    def process_file(self, source_path):
        tries = 0
        while tries < 5:
            if self.is_file_ready(source_path):
                break
            time.sleep(1)
            tries += 1
        else:
            logging.error(f"File {source_path} is not ready after multiple attempts.")
            return

        filename = os.path.basename(source_path)
        extension = os.path.splitext(filename)[1].lower()
        destination_dir = config['folders'].get(extension)
        
        if destination_dir:
            os.makedirs(destination_dir, exist_ok=True)
            date_folder = datetime.now().strftime("%Y-%m-%d")
            new_name = f"{date_folder}_{filename}"
            destination = os.path.join(destination_dir, new_name)
            
            try:
                shutil.move(source_path, destination)
                logging.info(f"File organized: {filename}")
            except Exception as e:
                logging.error(f"Error occurred while organizing file {filename}: {e}")

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