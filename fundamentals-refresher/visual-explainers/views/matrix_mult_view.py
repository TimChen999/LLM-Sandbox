"""Matrix multiplication animation — auto-plays through cells one at a time."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

from modules.linear_algebra import matrix_multiply_steps
from views._helpers import LabeledSlider


class MatrixMultView(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)

        self.a_rows = tk.IntVar(value=3)
        self.a_cols = tk.IntVar(value=3)
        self.b_cols = tk.IntVar(value=3)
        self.seed = tk.IntVar(value=0)
        self.speed_ms = tk.IntVar(value=600)

        self.steps: list[tuple[int, int, np.ndarray, np.ndarray, float]] = []
        self.step_idx = 0
        self.playing = False
        self._after_id: str | None = None

        self._build_controls()
        self._build_plot()
        self._regenerate()

    def _build_controls(self) -> None:
        bar = ttk.Frame(self, padding=(8, 8))
        bar.pack(side="top", fill="x")

        def labeled_spin(parent, label, var, lo, hi, callback):
            box = ttk.Frame(parent)
            ttk.Label(box, text=label).pack(side="left", padx=(0, 4))
            sp = ttk.Spinbox(box, from_=lo, to=hi, textvariable=var, width=4, command=callback)
            sp.pack(side="left", padx=(0, 12))
            return box

        labeled_spin(bar, "rows of A", self.a_rows, 2, 5, self._regenerate).pack(side="left")
        labeled_spin(bar, "cols of A = rows of B", self.a_cols, 2, 5, self._regenerate).pack(side="left")
        labeled_spin(bar, "cols of B", self.b_cols, 2, 5, self._regenerate).pack(side="left")
        labeled_spin(bar, "seed", self.seed, 0, 9999, self._regenerate).pack(side="left")

        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=8)

        self.play_btn = ttk.Button(bar, text="▶ Play", command=self._toggle_play)
        self.play_btn.pack(side="left", padx=2)
        ttk.Button(bar, text="⏮ Reset", command=self._reset).pack(side="left", padx=2)
        ttk.Button(bar, text="◀ Prev", command=self._step_back).pack(side="left", padx=2)
        ttk.Button(bar, text="Next ▶", command=self._step_forward).pack(side="left", padx=2)

        LabeledSlider(
            bar, "speed (ms/step)", self.speed_ms, 100, 1500, length=160, fmt="{:.0f}",
        ).pack(side="left", padx=(16, 4))

    def _build_plot(self) -> None:
        # IMPORTANT: pack the derivation panel FIRST (with side="bottom") so the
        # canvas (packed next with expand=True) doesn't steal the bottom space.
        derivation_frame = ttk.Frame(self, relief="groove", borderwidth=2, padding=(12, 8))
        derivation_frame.pack(side="bottom", fill="x")
        ttk.Label(
            derivation_frame, text="Derivation", font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")
        self.formula = ttk.Label(
            derivation_frame,
            text="",
            font=("Consolas", 12),
            justify="left",
            anchor="w",
        )
        self.formula.pack(fill="x", pady=(4, 0))

        self.fig = Figure(figsize=(11, 4.2), tight_layout=True)
        self.ax_a = self.fig.add_subplot(1, 3, 1)
        self.ax_b = self.fig.add_subplot(1, 3, 2)
        self.ax_c = self.fig.add_subplot(1, 3, 3)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ----- state changes -----

    def _regenerate(self) -> None:
        self._stop()
        rng = np.random.default_rng(int(self.seed.get()))
        self.A = rng.integers(-3, 4, size=(self.a_rows.get(), self.a_cols.get())).astype(float)
        self.B = rng.integers(-3, 4, size=(self.a_cols.get(), self.b_cols.get())).astype(float)
        self.C = np.full((self.a_rows.get(), self.b_cols.get()), np.nan)
        self.steps = list(matrix_multiply_steps(self.A, self.B))
        self.step_idx = 0
        self._redraw()

    def _reset(self) -> None:
        self._stop()
        self.C = np.full_like(self.C, np.nan)
        self.step_idx = 0
        self._redraw()

    def _step_forward(self) -> None:
        if self.step_idx < len(self.steps):
            i, j, _, _, v = self.steps[self.step_idx]
            self.C[i, j] = v
            self.step_idx += 1
            self._redraw()

    def _step_back(self) -> None:
        if self.step_idx > 0:
            self.step_idx -= 1
            i, j, _, _, _ = self.steps[self.step_idx]
            self.C[i, j] = np.nan
            self._redraw()

    def _toggle_play(self) -> None:
        if self.playing:
            self._stop()
        else:
            self._play()

    def _play(self) -> None:
        self.playing = True
        self.play_btn.configure(text="⏸ Pause")
        self._tick()

    def _stop(self) -> None:
        self.playing = False
        self.play_btn.configure(text="▶ Play")
        if self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None

    def _tick(self) -> None:
        if not self.playing:
            return
        if self.step_idx >= len(self.steps):
            self._stop()
            return
        self._step_forward()
        self._after_id = self.after(self.speed_ms.get(), self._tick)

    # ----- drawing -----

    def _redraw(self) -> None:
        cur = self.steps[self.step_idx - 1] if self.step_idx > 0 else None
        cur_i = cur[0] if cur else None
        cur_j = cur[1] if cur else None

        vmax = max(15.0, float(np.nanmax(np.abs(self.C))) if np.isfinite(self.C).any() else 15.0)
        self._draw_matrix(self.ax_a, self.A, "A", hl_row=cur_i)
        self._draw_matrix(self.ax_b, self.B, "B", hl_col=cur_j)
        self._draw_matrix(
            self.ax_c,
            self.C,
            f"C = A · B   (step {self.step_idx}/{len(self.steps)})",
            vmax=vmax,
        )
        self.canvas.draw_idle()

        if cur is not None:
            i, j, row, col, val = cur
            products = [f"({a:.0f})({b:.0f})" for a, b in zip(row, col)]
            partials = [f"{a * b:.0f}" for a, b in zip(row, col)]
            indent = " " * len(f"C[{i},{j}] ")
            lines = [
                f"C[{i},{j}] = (row {i} of A) · (col {j} of B)",
                f"{indent}= {' + '.join(products)}",
                f"{indent}= {' + '.join(partials)}",
                f"{indent}= {val:.0f}",
            ]
            self.formula.configure(text="\n".join(lines))
        else:
            self.formula.configure(
                text="Press ▶ Play to fill C cell-by-cell, or use Next ▶ to step through manually."
            )

    def _draw_matrix(self, ax, M, title, hl_row=None, hl_col=None, vmax=15.0):
        ax.clear()
        display = np.where(np.isnan(M), 0.0, M)
        ax.imshow(display, cmap="RdBu_r", vmin=-vmax, vmax=vmax, alpha=0.5)
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                v = M[i, j]
                ax.text(
                    j,
                    i,
                    "" if np.isnan(v) else f"{v:.0f}",
                    ha="center",
                    va="center",
                    fontsize=14,
                )
        if hl_row is not None:
            ax.add_patch(
                Rectangle(
                    (-0.5, hl_row - 0.5),
                    M.shape[1],
                    1,
                    fill=False,
                    edgecolor="orange",
                    linewidth=3,
                )
            )
        if hl_col is not None:
            ax.add_patch(
                Rectangle(
                    (hl_col - 0.5, -0.5),
                    1,
                    M.shape[0],
                    fill=False,
                    edgecolor="orange",
                    linewidth=3,
                )
            )
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
