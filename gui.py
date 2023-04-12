import os.path
import tkinter as tk

from tkinter import filedialog
from functools import partial

from pdf_utils import generate_composite_pdf, save_pdf

class GuiApp:
    def __init__(self, window, *a, **kw):
        super().__init__(*a, **kw)
        self._window = window

        self._window.title("PDF Merge Tool")
        self._window.geometry("400x400")
        self._window.config(bg="#ffffff")
        self._window.resizable(0,0)

        self._create_widgets()

        self._selected_files = []

        self._allowed_filetypes = (
            ("PDF", "*.pdf"),
        )


    def _select_files(self):
        self._selected_files = filedialog.askopenfilenames(
            title="Select files",
            filetypes=self._allowed_filetypes,
            multiple=True,
            parent=self._window,
        )

        if not self._selected_files:
            self._selected_files = []

        self._filename_label.delete(1.0, tk.END)

        filenames = [os.path.split(path)[1] for path in self._selected_files]
        self._filename_label.insert(
            tk.END,
            "\n".join([f"{i+1}. {fname}" for i, fname in enumerate(filenames)]),
        )

    def _generate(self):
        composite_pdf = generate_composite_pdf(self._selected_files)

        output_file = filedialog.asksaveasfilename(
            title="Save as",
            filetypes=self._allowed_filetypes,
            initialfile = "ShippingLabels.pdf",
            defaultextension=".pdf",
            parent=self._window,
        )

        save_pdf(composite_pdf, output_file)

    def _create_widgets(self):
        open_button = tk.Button(
            self._window,
            text="Select Files with Shipping Labels",
            command=self._select_files,
            bg="white",
        )
        open_button.pack(expand=True)

        self._filename_label = tk.Text(self._window, height=10, width=50)
        self._filename_label.delete(1.0, tk.END)
        self._filename_label.pack(expand=True)

        generate_button = tk.Button(
            self._window,
            text="Generate",
            command=self._generate,
            bg="white",
        )
        generate_button.pack(expand=True)

def run_gui():
    window = tk.Tk()
    app = GuiApp(window)

    window.attributes("-topmost", True)
    window.mainloop()
