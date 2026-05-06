"""Visual Explainers — Linear Algebra Curriculum.

A native Tk desktop app: home page + sidebar nav + topic pages.
Run dev: python app.py
Build .exe: build.bat
"""
from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk

sys.path.insert(0, str(Path(__file__).parent))

from curriculum import TOPICS
from curriculum.home import HomeFrame


class App(tk.Tk):
    SIDEBAR_WIDTH = 260
    ACCENT = "#2563eb"

    def __init__(self) -> None:
        super().__init__()
        self.title("Linear Algebra Curriculum — Visual Explainers")
        self.geometry("1500x950")
        self.minsize(1100, 700)
        try:
            ttk.Style(self).theme_use("vista")
        except tk.TclError:
            pass

        self._sidebar_buttons: dict[str, ttk.Button] = {}
        self._current_frame: tk.Widget | None = None
        self._build_ui()
        self.show_home()

    def _build_ui(self) -> None:
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        sidebar = ttk.Frame(self, width=self.SIDEBAR_WIDTH, padding=(0, 0))
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        ttk.Label(
            sidebar,
            text="Linear Algebra",
            font=("Segoe UI", 13, "bold"),
            padding=(16, 14, 16, 4),
        ).pack(anchor="w", fill="x")
        ttk.Label(
            sidebar,
            text="Refresher curriculum",
            font=("Segoe UI", 9),
            foreground="#666",
            padding=(16, 0, 16, 12),
        ).pack(anchor="w", fill="x")
        ttk.Separator(sidebar, orient="horizontal").pack(fill="x")

        self._sidebar_buttons["home"] = self._sidebar_button(
            sidebar, "  Home", self.show_home
        )
        ttk.Separator(sidebar, orient="horizontal").pack(fill="x", pady=(6, 6))

        for i, topic_cls in enumerate(TOPICS, start=1):
            label = f"  {i:>2}. {topic_cls.TITLE}"
            self._sidebar_buttons[topic_cls.__name__] = self._sidebar_button(
                sidebar, label, lambda c=topic_cls: self.show_topic(c)
            )

        self.content = ttk.Frame(self)
        self.content.grid(row=0, column=1, sticky="nsew")

    def _sidebar_button(self, parent: tk.Misc, text: str, command) -> ttk.Button:
        btn = ttk.Button(parent, text=text, command=command, style="Sidebar.TButton")
        btn.pack(fill="x", padx=8, pady=1, anchor="w")
        return btn

    def _swap(self, new_frame: tk.Widget) -> None:
        if self._current_frame is not None:
            self._current_frame.destroy()
        self._current_frame = new_frame
        new_frame.pack(fill="both", expand=True)

    def show_home(self) -> None:
        self._swap(HomeFrame(self.content, on_topic=self.show_topic))

    def show_topic(self, topic_cls) -> None:
        self._swap(topic_cls(self.content))


def main() -> None:
    App().mainloop()


if __name__ == "__main__":
    main()
