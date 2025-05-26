import tkinter as tk
from tkinter import ttk, filedialog

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sound File Organizer")
        self.geometry("500x450")
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        # internal list of files
        self.files = []

        # Top label
        ttk.Label(self, text="Upload and Arrange Sound Files").pack(pady=10)

        # Frame for listbox and scrollbar
        list_frame = ttk.Frame(self)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.file_list = tk.Listbox(list_frame, height=8)
        self.file_list.pack(side='left', fill='both', expand=True)
        scroll = ttk.Scrollbar(list_frame, command=self.file_list.yview)
        scroll.pack(side='right', fill='y')
        self.file_list.configure(yscrollcommand=scroll.set)

        # Button frame
        control_frame = ttk.Frame(self)
        control_frame.pack(pady=5)
        ttk.Button(control_frame, text="Add Files", command=self.add_files).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Move Up", command=lambda: self.move_item(-1)).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Move Down", command=lambda: self.move_item(1)).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Remove", command=self.remove_selected).pack(side='left', padx=5)

        # Progress bar demonstrates progress element
        self.progress = ttk.Progressbar(self, orient='horizontal', mode='determinate', length=200)
        self.progress.pack(pady=10)
        ttk.Button(self, text="Increase Progress", command=self.increase_progress).pack(pady=5)

        # Status label
        self.status = ttk.Label(self, text="Status: Ready")
        self.status.pack(pady=10)

    def add_files(self):
        paths = filedialog.askopenfilenames(
            title="Select sound files",
            filetypes=[("Sound Files", "*.wav *.mp3 *.flac *.ogg"), ("All files", "*.*")],
        )
        for path in paths:
            if path not in self.files:
                self.files.append(path)
                self.file_list.insert(tk.END, path)
        if paths:
            self.update_status(f"Added {len(paths)} file(s)")

    def move_item(self, direction: int):
        selection = self.file_list.curselection()
        if not selection:
            return
        index = selection[0]
        new_index = index + direction
        if 0 <= new_index < len(self.files):
            # swap in list
            self.files[index], self.files[new_index] = self.files[new_index], self.files[index]
            # update listbox
            self.file_list.delete(0, tk.END)
            for f in self.files:
                self.file_list.insert(tk.END, f)
            self.file_list.select_set(new_index)
            self.update_status("Reordered files")

    def remove_selected(self):
        selection = self.file_list.curselection()
        if not selection:
            return
        index = selection[0]
        removed = self.files.pop(index)
        self.file_list.delete(index)
        self.update_status(f"Removed {removed}")

    def update_status(self, message: str):
        self.status.config(text=f"Status: {message}")

    def increase_progress(self):
        value = (self.progress['value'] + 10) % 110
        self.progress['value'] = value
        self.update_status(f"Progress set to {value}%")

if __name__ == "__main__":
    app = App()
    app.mainloop()
