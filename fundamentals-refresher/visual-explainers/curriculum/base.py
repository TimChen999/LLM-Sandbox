"""TopicFrame: standard layout for every curriculum topic page."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from curriculum.practice_widget import PracticeWidget


class TopicFrame(ttk.Frame):
    """Base class for curriculum topic pages.

    Each subclass sets TITLE / BUILDS_ON / OVERVIEW and implements:
      - build_demo(parent): populate the Demo tab
      - build_practice(parent): populate the Practice tab
    """

    TITLE: str = ""
    BUILDS_ON: str = ""
    OVERVIEW: str = ""

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self._build()

    # ------- subclass hooks -------
    def build_demo(self, parent: tk.Misc) -> None:
        ttk.Label(parent, text="(no demo yet)", padding=(20, 20)).pack()

    def build_practice(self, parent: tk.Misc) -> None:
        ttk.Label(parent, text="(no practice yet)", padding=(20, 20)).pack()

    # ------- layout -------
    def _build(self) -> None:
        header = ttk.Frame(self, padding=(20, 16, 20, 12))
        header.pack(side="top", fill="x")
        ttk.Label(
            header, text=self.TITLE, font=("Segoe UI", 18, "bold")
        ).pack(anchor="w")
        if self.BUILDS_ON:
            ttk.Label(
                header,
                text=f"Builds on: {self.BUILDS_ON}",
                font=("Segoe UI", 9, "italic"),
                foreground="#555",
            ).pack(anchor="w", pady=(2, 0))
        if self.OVERVIEW:
            ttk.Label(
                header,
                text=self.OVERVIEW,
                font=("Segoe UI", 10),
                wraplength=1100,
                justify="left",
            ).pack(anchor="w", pady=(10, 0), fill="x")

        ttk.Separator(self, orient="horizontal").pack(fill="x")

        nb = ttk.Notebook(self)
        nb.pack(side="top", fill="both", expand=True, padx=12, pady=8)

        demo = ttk.Frame(nb)
        practice = ttk.Frame(nb)
        nb.add(demo, text="  Demo  ")
        nb.add(practice, text="  Practice  ")

        self.build_demo(demo)
        self.build_practice(practice)

    # ------- helper for subclasses -------
    def add_practice(self, parent: tk.Misc, generator) -> None:
        PracticeWidget(parent, generator).pack(fill="both", expand=True)
