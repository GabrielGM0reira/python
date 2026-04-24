import os
import shutil

file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Music": [".mp3", ".wav"],
    "Compressed": [".zip", ".rar"],
    "Scripts": [".py", ".js", ".html"]
}

def sortByType(path):
    for file in os.listdir(path):
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

                    shutil.move(file_path, folder_path)
                    print(f"Moved: {file} → {folder}")
                    moved = True
                    break

            if not moved:
                other_folder = os.path.join(path, "Others")
                if not os.path.exists(other_folder):
                    os.makedirs(other_folder)
                shutil.move(file_path, other_folder)
                print(f"Moved: {file} → Others")