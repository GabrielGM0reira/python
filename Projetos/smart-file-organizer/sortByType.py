import os
import shutil

def get_unique_path(path):
    """Generate unique file path if file already exists"""
    if not os.path.exists(path):
        return path
    
    base, ext = os.path.splitext(path)
    counter = 1
    while os.path.exists(f"{base}_{counter}{ext}"):
        counter += 1
    return f"{base}_{counter}{ext}"

file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Music": [".mp3", ".wav"],
    "Compressed": [".zip", ".rar"],
    "Scripts": [".py", ".js", ".html"]
}

def sortByType(path, logger=print, progress_callback=None):
    files = os.listdir(path)
    total = len(files)

    for index, file in enumerate(files, start=1):
        filename, ext = os.path.splitext(file)
        ext = ext.lower()
        file_path = os.path.join(path, file)

        if os.path.isfile(file_path):
            moved = False

            for folder, extensions in file_types.items():
                if ext in extensions:
                    folder_path = os.path.join(path, folder)

                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)

                    dest_path = os.path.join(folder_path, file)
                    dest_path = get_unique_path(dest_path)
                    shutil.move(file_path, dest_path)
                    logger(f"Moved: {file} → {folder}")
                    moved = True
                    break

            if not moved:
                other_folder = os.path.join(path, "Others")
                if not os.path.exists(other_folder):
                    os.makedirs(other_folder)
                dest_path = os.path.join(other_folder, file)
                dest_path = get_unique_path(dest_path)
                shutil.move(file_path, dest_path)
                logger(f"Moved: {file} → Others")

        if progress_callback:
            progress_callback(index, total)