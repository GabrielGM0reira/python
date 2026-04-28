import os
import shutil
from datetime import datetime

def get_unique_path(path):
    """Generate unique file path if file already exists"""
    if not os.path.exists(path):
        return path
    
    base, ext = os.path.splitext(path)
    counter = 1
    while os.path.exists(f"{base}_{counter}{ext}"):
        counter += 1
    return f"{base}_{counter}{ext}"

def sortByDate(path, logger=print, progress_callback=None):
    files = os.listdir(path)
    total = len(files)

    for index, file in enumerate(files, start=1):
        file_path = os.path.join(path, file)

        if os.path.isfile(file_path):
            modified = os.path.getmtime(file_path)
            date = datetime.fromtimestamp(modified).strftime("%Y-%m-%d")
            date_folder = os.path.join(path, date)

            if not os.path.exists(date_folder):
                os.makedirs(date_folder)

            dest_path = os.path.join(date_folder, file)
            dest_path = get_unique_path(dest_path)
            shutil.move(file_path, dest_path)
            logger(f"Moved: {file} → {date}")

        if progress_callback:
            progress_callback(index, total)