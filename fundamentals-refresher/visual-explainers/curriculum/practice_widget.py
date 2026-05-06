"""Reusable practice widget: random problem + reveal answer."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

import numpy as np

ProblemFn = Callable[[np.random.Generator], tuple[str, str]]


class PracticeWidget(ttk.Frame):
    def __init__(self, master: tk.Misc, generator: ProblemFn) -> None:
        super().__init__(master, padding=(24, 18))
        self._generator = generator
        self._rng = np.random.default_rng()
        self._answer = ""
        self._build()
        self.new_problem()

    def _build(self) -> None:
        bar = ttk.Frame(self)
        bar.pack(fill="x")
        ttk.Button(bar, text="🎲 New Problem", command=self.new_problem).pack(side="left")
        ttk.Button(bar, text="Show Answer", command=self.reveal).pack(side="left", padx=8)
        ttk.Label(
            bar,
            text="Try the problem on paper, then click Show Answer.",
            font=("Segoe UI", 9, "italic"),
            foreground="#666",
        ).pack(side="left", padx=12)

        prompt_frame = ttk.LabelFrame(self, text="  Problem  ", padding=(14, 10))
        prompt_frame.pack(fill="x", pady=(14, 8))
        self._prompt = ttk.Label(
            prompt_frame,
            text="",
            font=("Consolas", 12),
            justify="left",
            anchor="w",
            wraplength=1000,
        )
        self._prompt.pack(fill="x")

        answer_frame = ttk.LabelFrame(self, text="  Answer  ", padding=(14, 10))
        answer_frame.pack(fill="x")
        self._answer_lbl = ttk.Label(
            answer_frame,
            text="",
            font=("Consolas", 12),
            justify="left",
            anchor="w",
            wraplength=1000,
            foreground="#0d7d2e",
        )
        self._answer_lbl.pack(fill="x")

    def new_problem(self) -> None:
        prompt, self._answer = self._generator(self._rng)
        self._prompt.configure(text=prompt)
        self._answer_lbl.configure(text="")

    def reveal(self) -> None:
        self._answer_lbl.configure(text=self._answer)
