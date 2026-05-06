"""Visual Explainers — native Tk app entry point.

Run in dev: python app.py
Build to .exe: build.bat
"""
from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk

# Make sibling packages importable when frozen by PyInstaller and in dev.
sys.path.insert(0, str(Path(__file__).parent))

from views.linear_algebra_tab import LinearAlgebraTab


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Visual Explainers — ML Fundamentals")
        self.geometry("1200x800")
        self.minsize(900, 600)

        try:
            style = ttk.Style(self)
            style.theme_use("vista" if "vista" in style.theme_names() else style.theme_use())
        except tk.TclError:
            pass

        self._build_ui()

    def _build_ui(self) -> None:
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        notebook.add(LinearAlgebraTab(notebook), text="Linear Algebra")
        # Future: notebook.add(ProbabilityTab(notebook), text="Probability")
        # Future: notebook.add(OptimizationTab(notebook), text="Optimization")


def main() -> None:
    App().mainloop()


if __name__ == "__main__":
    main()
