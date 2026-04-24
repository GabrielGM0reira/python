import os
import hashlib
import shutil

def hash_file(file_path):
    h = hashlib.md5()
    with open(file_path, "rb") as f:
        chunk = f.read(8192)
        while chunk:
            h.update(chunk)
            chunk = f.read(8192)
    return h.hexdigest()

def find_duplicates(path):
    duplicates_folder = os.path.join(path, "Duplicates")
    if not os.path.exists(duplicates_folder):
        os.makedirs(duplicates_folder)

    hashes = {}

    for file in os.listdir(path):
        file_path = os.path.join(path, file)

        if os.path.isfile(file_path):
            file_hash = hash_file(file_path)

            if file_hash in hashes:
                shutil.move(file_path, duplicates_folder)
                print(f"Duplicate Found: {file} → moved to Duplicates")
            else:
                hashes[file_hash] = file