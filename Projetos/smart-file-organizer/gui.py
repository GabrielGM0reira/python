import tkinter as tk
from tkinter import filedialog
import organizer

def choose_folder():
    folder = filedialog.askdirectory()
    label.config(text=f"Selected: {folder}")
    organizer.run_all(folder)

root = tk.Tk()
root.title("Smart File Organizer")
root.geometry("420x200")

label = tk.Label(root, text="Choose a folder to organize", font=("Arial", 13))
label.pack(pady=20)

btn = tk.Button(root, text="Select Folder", command=choose_folder, width=20)
btn.pack()

root.mainloop()