"""Front page: welcome + clickable cards for each topic."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from curriculum import TOPICS


class HomeFrame(ttk.Frame):
    CARD_BG = "#f7f8fa"
    CARD_HOVER_BG = "#eef2ff"

    def __init__(self, master: tk.Misc, on_topic: Callable[[type], None]) -> None:
        super().__init__(master)
        self.on_topic = on_topic
        self._build()

    def _build(self) -> None:
        # Scrollable canvas
        canvas = tk.Canvas(self, highlightthickness=0, bg="white")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        inner = ttk.Frame(canvas)
        inner.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=inner, anchor="nw", tags="inner")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_canvas_resize(e):
            canvas.itemconfigure("inner", width=e.width)

        canvas.bind("<Configure>", _on_canvas_resize)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-e.delta / 120), "units"))

        # Hero
        hero = ttk.Frame(inner, padding=(40, 32, 40, 16))
        hero.pack(fill="x")
        ttk.Label(
            hero,
            text="Linear Algebra Curriculum",
            font=("Segoe UI", 26, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            hero,
            text="A visual, interactive refresher of the linear-algebra concepts that power ML.",
            font=("Segoe UI", 12),
            foreground="#444",
        ).pack(anchor="w", pady=(6, 0))
        ttk.Label(
            hero,
            text=(
                "Each topic has three parts: a short overview (what + why for ML), "
                "a visual demo with step-by-step calculations, and randomly generated "
                "practice problems. Topics build on each other; the sidebar shows the order."
            ),
            font=("Segoe UI", 10),
            wraplength=1100,
            foreground="#444",
            justify="left",
        ).pack(anchor="w", pady=(12, 0))

        ttk.Separator(inner, orient="horizontal").pack(fill="x", padx=40, pady=(20, 8))

        ttk.Label(
            inner,
            text="Topics",
            font=("Segoe UI", 14, "bold"),
            padding=(40, 8, 40, 4),
        ).pack(anchor="w")

        # Cards grid (2 columns)
        grid = ttk.Frame(inner, padding=(36, 8, 36, 36))
        grid.pack(fill="both", expand=True)
        for col in (0, 1):
            grid.columnconfigure(col, weight=1, uniform="card")

        for idx, topic_cls in enumerate(TOPICS):
            r, c = divmod(idx, 2)
            self._make_card(grid, idx + 1, topic_cls).grid(
                row=r, column=c, sticky="nsew", padx=8, pady=8
            )

    def _make_card(self, parent: tk.Misc, num: int, topic_cls) -> ttk.Frame:
        card = tk.Frame(
            parent,
            bg=self.CARD_BG,
            highlightthickness=1,
            highlightbackground="#d0d7de",
            cursor="hand2",
        )
        # Layout
        inner = tk.Frame(card, bg=self.CARD_BG, padx=18, pady=14)
        inner.pack(fill="both", expand=True)

        tk.Label(
            inner,
            text=f"{num:>2}",
            font=("Segoe UI", 20, "bold"),
            fg="#2563eb",
            bg=self.CARD_BG,
        ).pack(anchor="w")
        tk.Label(
            inner,
            text=topic_cls.TITLE,
            font=("Segoe UI", 13, "bold"),
            bg=self.CARD_BG,
            anchor="w",
            justify="left",
            wraplength=480,
        ).pack(anchor="w", pady=(2, 6), fill="x")

        # Trim overview to 2 lines worth.
        ov = topic_cls.OVERVIEW.strip().split("\n")[0]
        tk.Label(
            inner,
            text=ov,
            font=("Segoe UI", 10),
            bg=self.CARD_BG,
            fg="#444",
            anchor="w",
            justify="left",
            wraplength=480,
        ).pack(anchor="w", fill="x")

        if topic_cls.BUILDS_ON:
            tk.Label(
                inner,
                text=f"Builds on: {topic_cls.BUILDS_ON}",
                font=("Segoe UI", 9, "italic"),
                bg=self.CARD_BG,
                fg="#666",
                anchor="w",
            ).pack(anchor="w", pady=(8, 0), fill="x")

        # Click & hover behavior on every child
        def on_click(_event=None, c=topic_cls):
            self.on_topic(c)

        def on_enter(_event=None):
            for w in (card, inner, *inner.winfo_children()):
                try:
                    w.configure(bg=self.CARD_HOVER_BG)
                except tk.TclError:
                    pass

        def on_leave(_event=None):
            for w in (card, inner, *inner.winfo_children()):
                try:
                    w.configure(bg=self.CARD_BG)
                except tk.TclError:
                    pass

        for w in (card, inner, *inner.winfo_children()):
            w.bind("<Button-1>", on_click)
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)

        return card
