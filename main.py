import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sound File Uploader")
        self.geometry("400x150")

        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        ttk.Label(self, text="Select a sound file to upload").pack(pady=10)

        self.file_path = tk.StringVar()
        ttk.Entry(self, textvariable=self.file_path, width=40, state='readonly').pack(padx=10)
        ttk.Button(self, text="Browse", command=self.browse).pack(pady=10)

    def browse(self):
        filetypes = [("Sound files", "*.wav *.mp3 *.ogg *.flac *.aac")]
        path = filedialog.askopenfilename(title="Choose a sound file", filetypes=filetypes)
        if not path:
            return
        ext = os.path.splitext(path)[1].lower()
        if ext in {".wav", ".mp3", ".ogg", ".flac", ".aac"}:
            self.file_path.set(path)
        else:
            messagebox.showerror("Invalid file", "Please select a supported sound file.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
