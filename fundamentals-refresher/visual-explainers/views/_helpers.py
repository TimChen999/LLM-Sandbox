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


class MatrixSliders(ttk.Frame):
    """A grid of LabeledSliders arranged to mirror a matrix's shape.

    `vars_grid` is a list of rows; each row is a list of tk variables. The
    sliders end up at the same (row, col) position as the matrix entry they
    edit, so the spatial layout itself shows what A[i, j] means.
    """

    def __init__(
        self,
        master: tk.Misc,
        vars_grid: list[list[tk.DoubleVar | tk.IntVar]],
        from_: float,
        to: float,
        name: str = "A",
        length: int = 110,
        command=None,
    ) -> None:
        super().__init__(master)
        # Optional title above the grid
        if name:
            ttk.Label(
                self,
                text=f"matrix {name}  (label = [row, col])",
                font=("Segoe UI", 9, "italic"),
                foreground="#555",
            ).grid(row=0, column=0, columnspan=len(vars_grid[0]), sticky="w", padx=2)
        for r, row in enumerate(vars_grid, start=1):
            for c, var in enumerate(row):
                LabeledSlider(
                    self,
                    label=f"{name}[{r - 1},{c}]",
                    var=var,
                    from_=from_,
                    to=to,
                    length=length,
                    command=command,
                ).grid(row=r, column=c, padx=4, pady=2)
