"""Shared widget helpers for views."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable


class LabeledSlider(ttk.Frame):
    """A slider with a label above and a live numeric readout below.

    The numeric readout updates whenever the variable changes (i.e. while the
    user drags the slider), so the user can always see the current value.
    """

    VALUE_COLOR = "#1d4ed8"

    def __init__(
        self,
        master: tk.Misc,
        label: str,
        var: tk.DoubleVar | tk.IntVar,
        from_: float,
        to: float,
        length: int = 130,
        command: Callable[..., None] | None = None,
        fmt: str = "{:+.2f}",
    ) -> None:
        super().__init__(master)
        self._var = var
        self._fmt = fmt

        ttk.Label(self, text=label, font=("Segoe UI", 9)).pack()
        ttk.Scale(
            self,
            from_=from_,
            to=to,
            variable=var,
            orient="horizontal",
            length=length,
            command=command,
        ).pack()
        self._value_lbl = ttk.Label(
            self,
            text=self._format(),
            font=("Consolas", 10, "bold"),
            foreground=self.VALUE_COLOR,
            width=7,
            anchor="center",
        )
        self._value_lbl.pack()
        var.trace_add("write", self._on_var_change)

    def _format(self) -> str:
        try:
            return self._fmt.format(float(self._var.get()))
        except Exception:
            return str(self._var.get())

    def _on_var_change(self, *_: object) -> None:
        self._value_lbl.configure(text=self._format())
