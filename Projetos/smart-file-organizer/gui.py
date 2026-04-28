import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
import organizer
import threading

class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart File Organizer")
        self.root.geometry("640x620")
        self.selected_folder = ""
        self.is_running = False
        
        # Top frame: folder selection
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.folder_label = tk.Label(top_frame, text="No folder selected", 
                                     font=("Arial", 10), fg="gray")
        self.folder_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        btn_browse = tk.Button(top_frame, text="Browse", command=self.choose_folder, width=12)
        btn_browse.pack(side=tk.RIGHT, padx=5)
        
        # Separator
        tk.Frame(root, height=2, bg="#CCCCCC").pack(fill=tk.X, padx=10)
        
        # Options frame: select operations
        options_frame = tk.LabelFrame(root, text="Operations", font=("Arial", 10, "bold"))
        options_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.var_type = tk.BooleanVar(value=True)
        self.var_date = tk.BooleanVar(value=True)
        self.var_dups = tk.BooleanVar(value=True)
        
        tk.Checkbutton(options_frame, text="Sort by Type", variable=self.var_type).pack(anchor=tk.W, padx=8, pady=2)
        tk.Checkbutton(options_frame, text="Sort by Date", variable=self.var_date).pack(anchor=tk.W, padx=8, pady=2)
        tk.Checkbutton(options_frame, text="Find Duplicates", variable=self.var_dups).pack(anchor=tk.W, padx=8, pady=2)
        
        # Output frame: status and logs
        output_frame = tk.LabelFrame(root, text="Status", font=("Arial", 10, "bold"))
        output_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=16, width=78, 
                                                     font=("Courier", 10), state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Progress bar frame
        progress_frame = tk.Frame(root)
        progress_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.progress_label = tk.Label(progress_frame, text="Ready", font=("Arial", 10))
        self.progress_label.pack(side=tk.LEFT, padx=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, mode="determinate", maximum=100)
        self.progress_bar.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Bottom frame: action buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10, fill=tk.X, padx=10)
        
        self.btn_run = tk.Button(btn_frame, text="Start Organizing", command=self.run_organize, 
                                 bg="#2E8B57", fg="white", width=22)
        self.btn_run.pack(side=tk.LEFT, padx=5)
        
        btn_clear = tk.Button(btn_frame, text="Clear Log", command=self.clear_log, width=18)
        btn_clear.pack(side=tk.LEFT, padx=5)
    
    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder = folder
            self.folder_label.config(text=folder, fg="black")
            self.log(f"✓ Folder selected: {folder}")
    
    def log(self, message):
        """Append message to output text widget"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the output text widget"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.progress_bar['value'] = 0
        self.progress_label.config(text="Ready")
    
    def run_organize(self):
        """Run organization in a separate thread"""
        if not self.selected_folder:
            self.log("❌ Error: Please select a folder first!")
            return
        
        if self.is_running:
            self.log("⚠ Already running...")
            return
        
        selected_tasks = [
            task for task, var in [
                ("type", self.var_type),
                ("date", self.var_date),
                ("duplicates", self.var_dups)
            ] if var.get()
        ]
        if not selected_tasks:
            self.log("⚠ Please choose at least one operation.")
            return
        
        self.is_running = True
        self.btn_run.config(state=tk.DISABLED, text="Running...", bg="#999999")
        self.clear_log()
        self.progress_bar['value'] = 0
        self.progress_label.config(text="Starting...")
        
        thread = threading.Thread(target=self._organize_thread, args=(selected_tasks,), daemon=True)
        thread.start()
    
    def _organize_thread(self, selected_tasks):
        """Execute organization tasks in background thread"""
        try:
            path = self.selected_folder
            total_tasks = len(selected_tasks)
            
            def progress_callback(current, total, task_index, task_count, task_name):
                task_percent = int((current / total) * 100) if total else 0
                overall = int(((task_index - 1) + current / total) / task_count * 100)
                def update_ui():
                    self.progress_bar['value'] = overall
                    self.progress_label.config(text=f"{task_name}: {task_percent}%")
                self.root.after(0, update_ui)
            
            def build_progress(task_index, task_count, task_name):
                return lambda current, total: progress_callback(current, total, task_index, task_count, task_name)
            
            def run_selected_tasks():
                if "type" in selected_tasks:
                    organizer.run_all(path, logger=self.log, progress_callback=build_progress(selected_tasks.index("type") + 1, total_tasks, "Sort by Type"), selected_tasks=["type"])
                if "date" in selected_tasks:
                    organizer.run_all(path, logger=self.log, progress_callback=build_progress(selected_tasks.index("date") + 1, total_tasks, "Sort by Date"), selected_tasks=["date"])
                if "duplicates" in selected_tasks:
                    organizer.run_all(path, logger=self.log, progress_callback=build_progress(selected_tasks.index("duplicates") + 1, total_tasks, "Find Duplicates"), selected_tasks=["duplicates"])
            
            run_selected_tasks()
            self.progress_bar['value'] = 100
            self.progress_label.config(text="Completed")
            self.log("\n✅ All selected tasks completed successfully!")
        except Exception as e:
            self.log(f"\n❌ Error: {str(e)}")
            self.progress_label.config(text="Error")
        finally:
            self.is_running = False
            self.btn_run.config(state=tk.NORMAL, text="Start Organizing", bg="#2E8B57")

root = tk.Tk()
app = FileOrganizerGUI(root)
root.mainloop()