"""Matrix calculus — gradient of f(x) = ½ xᵀ A x − bᵀ x as arrow on a contour plot."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from views._helpers import LabeledSlider


class MatrixCalculusDemo(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.a11 = tk.DoubleVar(value=2.0)
        self.a22 = tk.DoubleVar(value=1.0)
        self.a12 = tk.DoubleVar(value=0.4)
        self.bx = tk.DoubleVar(value=1.0)
        self.by = tk.DoubleVar(value=-0.5)
        self.point = np.array([1.0, 1.0])
        self._build_controls()
        self._build_plot()
        self._recompute()
        self.canvas.mpl_connect("button_press_event", self._on_click)

    def _build_controls(self) -> None:
        bar = ttk.Frame(self, padding=(8, 8))
        bar.pack(side="top", fill="x")
        ttk.Label(bar, text="A (sym):", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 6))
        for label, var in [("A[0,0]", self.a11), ("A[1,1]", self.a22), ("A[0,1]", self.a12)]:
            LabeledSlider(
                bar, label, var, -2, 3, length=120,
                command=lambda *_: self._recompute(),
            ).pack(side="left", padx=4)
        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=10)
        ttk.Label(bar, text="b:", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 6))
        for label, var in [("b.x", self.bx), ("b.y", self.by)]:
            LabeledSlider(
                bar, label, var, -3, 3, length=120,
                command=lambda *_: self._recompute(),
            ).pack(side="left", padx=4)
        ttk.Label(bar, text="↓ Click anywhere in the plot to set x.",
                  font=("Segoe UI", 9, "italic"), foreground="#0d7d2e").pack(side="left", padx=14)

    def _build_plot(self) -> None:
        derivation = ttk.LabelFrame(self, text="  Calculation  ", padding=(12, 8))
        derivation.pack(side="bottom", fill="x")
        self.calc = ttk.Label(derivation, text="", font=("Consolas", 11), justify="left", anchor="w")
        self.calc.pack(fill="x")

        self.fig = Figure(figsize=(7, 6), tight_layout=True)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _on_click(self, event) -> None:
        if event.inaxes is self.ax and event.xdata is not None and event.ydata is not None:
            self.point = np.array([event.xdata, event.ydata])
            self._redraw()

    def _recompute(self) -> None:
        self._redraw()

    def _redraw(self) -> None:
        A = np.array([[self.a11.get(), self.a12.get()],
                      [self.a12.get(), self.a22.get()]])
        b = np.array([self.bx.get(), self.by.get()])
        x = self.point

        n = 200
        xs = np.linspace(-3, 3, n)
        X, Y = np.meshgrid(xs, xs)
        F = 0.5 * (A[0, 0] * X**2 + 2 * A[0, 1] * X * Y + A[1, 1] * Y**2) - b[0] * X - b[1] * Y

        ax = self.ax
        ax.clear()
        ax.contour(X, Y, F, levels=20, cmap="RdBu_r", alpha=0.7)
        # Gradient arrow
        grad = A @ x - b
        ax.plot(x[0], x[1], "o", color="black", markersize=7)
        ax.quiver(x[0], x[1], grad[0], grad[1], angles="xy", scale_units="xy",
                  scale=1, color="C3", width=0.012, alpha=0.85)
        ax.text(x[0] + 0.1, x[1] + 0.1, "x", fontsize=12)
        # Newton step direction (− A⁻¹ grad), if A is invertible — points to the optimum
        try:
            xstar = np.linalg.solve(A, b)
            if np.all(np.abs(xstar) < 3):
                ax.plot(xstar[0], xstar[1], "*", color="green", markersize=14, label="x* = A⁻¹b")
                ax.legend(loc="upper left", fontsize=9)
        except np.linalg.LinAlgError:
            pass
        ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect("equal")
        ax.set_title("Contours of  f(x) = ½ xᵀAx − bᵀx     ∇f(x) = A x − b   (red arrow)")
        self.canvas.draw_idle()

        self.calc.configure(
            text=(
                f"f(x) = ½ xᵀAx − bᵀx\n"
                f"At x = ({x[0]:+.3f}, {x[1]:+.3f}):\n"
                f"  A x = ({(A@x)[0]:+.4f}, {(A@x)[1]:+.4f})\n"
                f"  ∇f  = A x − b = ({grad[0]:+.4f}, {grad[1]:+.4f})    "
                f"f(x) = {0.5 * x @ A @ x - b @ x:+.4f}\n"
                f"Setting ∇f = 0  ⇒  x* = A⁻¹ b  (when A is invertible) — green star."
            )
        )
