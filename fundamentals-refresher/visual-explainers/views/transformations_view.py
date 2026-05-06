"""Linear transformations — show the unit grid being transformed by a 2x2 matrix."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class TransformationsDemo(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.a11 = tk.DoubleVar(value=1.0)
        self.a12 = tk.DoubleVar(value=0.5)
        self.a21 = tk.DoubleVar(value=0.0)
        self.a22 = tk.DoubleVar(value=1.5)
        self.t = tk.DoubleVar(value=1.0)
        self._after_id: str | None = None
        self._build_controls()
        self._build_plot()
        self._recompute()

    def _build_controls(self) -> None:
        bar = ttk.Frame(self, padding=(8, 8))
        bar.pack(side="top", fill="x")
        for label, var in [
            ("A[0,0]", self.a11), ("A[0,1]", self.a12),
            ("A[1,0]", self.a21), ("A[1,1]", self.a22),
        ]:
            box = ttk.Frame(bar)
            ttk.Label(box, text=label).pack()
            ttk.Scale(
                box, from_=-2, to=2, variable=var, orient="horizontal", length=120,
                command=lambda *_: self._recompute()
            ).pack()
            box.pack(side="left", padx=6)

        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=8)
        ttk.Button(bar, text="▶ Animate identity → A", command=self._animate).pack(side="left", padx=4)
        ttk.Button(bar, text="↺ Reset to A", command=self._reset).pack(side="left", padx=4)

    def _build_plot(self) -> None:
        derivation = ttk.LabelFrame(self, text="  Calculation  ", padding=(12, 8))
        derivation.pack(side="bottom", fill="x")
        self.calc = ttk.Label(
            derivation, text="", font=("Consolas", 11), justify="left", anchor="w"
        )
        self.calc.pack(fill="x")

        self.fig = Figure(figsize=(11, 5), tight_layout=True)
        self.ax_orig = self.fig.add_subplot(1, 2, 1)
        self.ax_xform = self.fig.add_subplot(1, 2, 2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _recompute(self) -> None:
        self._cancel_animation()
        self._redraw()

    def _redraw(self) -> None:
        A_full = np.array(
            [[self.a11.get(), self.a12.get()], [self.a21.get(), self.a22.get()]]
        )
        t = self.t.get()
        I = np.eye(2)
        A = (1 - t) * I + t * A_full
        det = float(np.linalg.det(A))

        for ax, M, title in [(self.ax_orig, np.eye(2), "Original (unit grid)"),
                             (self.ax_xform, A, f"After A  (t={t:.2f})")]:
            ax.clear()
            self._draw_grid(ax, M)
            ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect("equal")
            ax.grid(alpha=0.2); ax.set_title(title)

        self.calc.configure(
            text=(
                f"A =  [[{A_full[0,0]:.2f}, {A_full[0,1]:.2f}],  [{A_full[1,0]:.2f}, {A_full[1,1]:.2f}]]\n"
                f"Each grid point (x, y) goes to (a·x + b·y, c·x + d·y) = "
                f"({A_full[0,0]:.2f}·x + {A_full[0,1]:.2f}·y, "
                f"{A_full[1,0]:.2f}·x + {A_full[1,1]:.2f}·y)\n"
                f"det(A) = a·d − b·c = "
                f"({A_full[0,0]:.2f})({A_full[1,1]:.2f}) − ({A_full[0,1]:.2f})({A_full[1,0]:.2f}) "
                f"= {np.linalg.det(A_full):+.4f}    "
                f"→ |det| is the area scale factor; sign indicates orientation."
            )
        )
        self.canvas.draw_idle()

    @staticmethod
    def _draw_grid(ax, A: np.ndarray) -> None:
        # Original grid lines
        n = 5
        for k in np.linspace(-2, 2, 9):
            line_h = np.array([[-2, k], [2, k]])
            line_v = np.array([[k, -2], [k, 2]])
            for line, color in [(line_h, "#9ec5fe"), (line_v, "#fdba74")]:
                pts = (A @ line.T).T
                ax.plot(pts[:, 0], pts[:, 1], color=color, lw=1, alpha=0.7)
        # Basis vectors
        e1 = A @ np.array([1, 0])
        e2 = A @ np.array([0, 1])
        ax.quiver(0, 0, e1[0], e1[1], angles="xy", scale_units="xy", scale=1, color="C0", width=0.012)
        ax.quiver(0, 0, e2[0], e2[1], angles="xy", scale_units="xy", scale=1, color="C1", width=0.012)
        ax.text(e1[0] * 1.05, e1[1] * 1.05, "Ae₁", color="C0", fontweight="bold")
        ax.text(e2[0] * 1.05, e2[1] * 1.05, "Ae₂", color="C1", fontweight="bold")

    def _animate(self) -> None:
        self._cancel_animation()
        self._anim_step = 0
        self._anim_total = 40
        self._tick()

    def _tick(self) -> None:
        if self._anim_step > self._anim_total:
            return
        self.t.set(self._anim_step / self._anim_total)
        self._redraw()
        self._anim_step += 1
        self._after_id = self.after(40, self._tick)

    def _reset(self) -> None:
        self._cancel_animation()
        self.t.set(1.0)
        self._redraw()

    def _cancel_animation(self) -> None:
        if self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None
