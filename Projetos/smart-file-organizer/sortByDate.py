import os
import shutil
from datetime import datetime

def sortByDate(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)

        if os.path.isfile(file_path):
            modified = os.path.getmtime(file_path)
            date = datetime.fromtimestamp(modified).strftime("%Y-%m-%d")
            date_folder = os.path.join(path, date)

            if not os.path.exists(date_folder):
                os.makedirs(date_folder)

            shutil.move(file_path, date_folder)
            print(f"Moved: {file} → {date}")