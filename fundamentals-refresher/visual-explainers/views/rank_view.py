"""Rank, null space, column space — visualize columns of a 2x3 matrix in 2D."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from views._helpers import LabeledSlider


class RankDemo(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        # 2 rows × 3 columns of A
        self.entries = [tk.DoubleVar(value=v) for v in [1.0, 2.0, 0.0, 0.0, 1.0, 1.0]]
        self._build_controls()
        self._build_plot()
        self._recompute()

    def _build_controls(self) -> None:
        bar = ttk.Frame(self, padding=(8, 8))
        bar.pack(side="top", fill="x")
        ttk.Label(bar, text="A (2×3) entries:", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 8))
        labels = ["A[0,0]", "A[0,1]", "A[0,2]", "A[1,0]", "A[1,1]", "A[1,2]"]
        for label, var in zip(labels, self.entries):
            LabeledSlider(
                bar, label, var, -3, 3, length=110,
                command=lambda *_: self._recompute(),
            ).pack(side="left", padx=4)
        ttk.Button(bar, text="Make rank 1", command=lambda: self._set_rank(1)).pack(side="left", padx=8)
        ttk.Button(bar, text="Make rank 2", command=lambda: self._set_rank(2)).pack(side="left", padx=4)

    def _set_rank(self, target: int) -> None:
        rng = np.random.default_rng()
        if target == 1:
            u = rng.integers(-2, 3, size=(2, 1))
            while np.all(u == 0):
                u = rng.integers(-2, 3, size=(2, 1))
            v = rng.integers(-2, 3, size=(1, 3))
            while np.all(v == 0):
                v = rng.integers(-2, 3, size=(1, 3))
            A = u @ v
        else:
            U = rng.integers(-2, 3, size=(2, 2))
            while np.linalg.matrix_rank(U) < 2:
                U = rng.integers(-2, 3, size=(2, 2))
            V = rng.integers(-2, 3, size=(2, 3))
            A = U @ V
        for var, val in zip(self.entries, A.flatten()):
            var.set(float(val))
        self._recompute()

    def _build_plot(self) -> None:
        derivation = ttk.LabelFrame(self, text="  Calculation  ", padding=(12, 8))
        derivation.pack(side="bottom", fill="x")
        self.calc = ttk.Label(derivation, text="", font=("Consolas", 11), justify="left", anchor="w")
        self.calc.pack(fill="x")

        self.fig = Figure(figsize=(7, 6), tight_layout=True)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _recompute(self) -> None:
        A = np.array([[self.entries[0].get(), self.entries[1].get(), self.entries[2].get()],
                      [self.entries[3].get(), self.entries[4].get(), self.entries[5].get()]])
        rank = int(np.linalg.matrix_rank(A))

        ax = self.ax
        ax.clear()
        ax.axhline(0, color="#999", lw=0.5)
        ax.axvline(0, color="#999", lw=0.5)
        ax.grid(alpha=0.25)

        # Plot column vectors
        colors = ["C0", "C1", "C2"]
        for j in range(3):
            c = A[:, j]
            ax.quiver(0, 0, c[0], c[1], angles="xy", scale_units="xy", scale=1,
                      color=colors[j], width=0.012, alpha=0.85)
            ax.text(c[0] * 1.05, c[1] * 1.05 + 0.1, f"col {j}", color=colors[j], fontsize=11)

        # Span visualization
        if rank == 1:
            nonzero = A[:, np.argmax(np.linalg.norm(A, axis=0))]
            t = np.linspace(-4, 4, 2)
            line = np.outer(t, nonzero)
            ax.plot(line[:, 0], line[:, 1], "--", color="#888", lw=1.5, alpha=0.7,
                    label="column space (line)")
        elif rank == 2:
            ax.fill([-4, 4, 4, -4], [-4, -4, 4, 4], color="#dbeafe", alpha=0.4,
                    label="column space (all of ℝ²)")
        ax.legend(loc="upper left", fontsize=9)
        ax.set_xlim(-4, 4); ax.set_ylim(-4, 4); ax.set_aspect("equal")
        ax.set_title(f"Columns of A (rank = {rank})")
        self.canvas.draw_idle()

        col_strs = [f"col {j} = ({A[0,j]:.1f}, {A[1,j]:.1f})" for j in range(3)]
        if rank == 0:
            interpretation = "All columns are zero — column space is just the origin."
        elif rank == 1:
            interpretation = "All columns are scalar multiples of one another → column space is a line. 2 of the 3 columns are linearly dependent."
        elif rank == 2:
            interpretation = "Columns span all of ℝ² → column space is the full plane. (One column is a linear combination of the other two — null space is 1-dim.)"
        else:
            interpretation = ""
        self.calc.configure(
            text=("\n".join(col_strs) +
                  f"\nrank(A) = {rank}    nullity = {3 - rank}    (rank + nullity = number of columns)\n"
                  f"{interpretation}")
        )
