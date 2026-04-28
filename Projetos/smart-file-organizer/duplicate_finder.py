import os
import hashlib
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

def hash_file(file_path):
    h = hashlib.md5()
    with open(file_path, "rb") as f:
        chunk = f.read(8192)
        while chunk:
            h.update(chunk)
            chunk = f.read(8192)
    return h.hexdigest()

def find_duplicates(path, logger=print, progress_callback=None):
    duplicates_folder = os.path.join(path, "Duplicates")
    if not os.path.exists(duplicates_folder):
        os.makedirs(duplicates_folder)

    hashes = {}
    files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    total = len(files)

    for index, file in enumerate(files, start=1):
        file_path = os.path.join(path, file)
        file_hash = hash_file(file_path)

        if file_hash in hashes:
            dest_path = os.path.join(duplicates_folder, file)
            dest_path = get_unique_path(dest_path)
            shutil.move(file_path, dest_path)
            logger(f"Duplicate Found: {file} → moved to Duplicates")
        else:
            hashes[file_hash] = file

        if progress_callback:
            progress_callback(index, total)