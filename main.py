import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Windows 11 GUI Demo")
        self.geometry("500x400")
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        
        # Label
        ttk.Label(self, text="This is a label demonstrating text output").pack(pady=10)
        
        # Scrollable text
        frame = ttk.Frame(self)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        text = tk.Text(frame, height=5, wrap='word')
        scroll = ttk.Scrollbar(frame, command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        sample_paragraph = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
            "Vestibulum interdum quam sit amet risus dictum, in egestas "
            "purus fermentum. Vestibulum ante ipsum primis in faucibus "
            "orci luctus et ultrices posuere cubilia curae."
        )
        text.insert('1.0', sample_paragraph)
        text.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Button 1", command=lambda: self.update_status("Button 1 pressed")).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Button 2", command=lambda: self.update_status("Button 2 pressed")).pack(side='left', padx=5)
        
        # Progress Bar
        self.progress = ttk.Progressbar(self, orient='horizontal', mode='determinate', length=200)
        self.progress.pack(pady=10)
        ttk.Button(self, text="Increase Progress", command=self.increase_progress).pack(pady=5)
        
        # Status label
        self.status = ttk.Label(self, text="Status: Ready")
        self.status.pack(pady=10)

    def update_status(self, message: str):
        self.status.config(text=f"Status: {message}")

    def increase_progress(self):
        value = (self.progress['value'] + 10) % 110
        self.progress['value'] = value
        self.update_status(f"Progress set to {value}%")

if __name__ == "__main__":
    app = App()
    app.mainloop()
