"""Projections — visualize projecting b onto the line spanned by u."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from views._helpers import LabeledSlider


class ProjectionsDemo(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.bx = tk.DoubleVar(value=3.0)
        self.by = tk.DoubleVar(value=2.0)
        self.ux = tk.DoubleVar(value=2.0)
        self.uy = tk.DoubleVar(value=0.5)
        self._build_controls()
        self._build_plot()
        self._recompute()

    def _build_controls(self) -> None:
        bar = ttk.Frame(self, padding=(8, 8))
        bar.pack(side="top", fill="x")
        ttk.Label(bar, text="target b:", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 8))
        LabeledSlider(bar, "b.x", self.bx, -5, 5, length=130, command=lambda *_: self._recompute()).pack(side="left", padx=6)
        LabeledSlider(bar, "b.y", self.by, -5, 5, length=130, command=lambda *_: self._recompute()).pack(side="left", padx=6)

        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=12)
        ttk.Label(bar, text="direction u:", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 8))
        LabeledSlider(bar, "u.x", self.ux, -5, 5, length=130, command=lambda *_: self._recompute()).pack(side="left", padx=6)
        LabeledSlider(bar, "u.y", self.uy, -5, 5, length=130, command=lambda *_: self._recompute()).pack(side="left", padx=6)

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
        b = np.array([self.bx.get(), self.by.get()])
        u = np.array([self.ux.get(), self.uy.get()])
        if np.linalg.norm(u) < 1e-9:
            return

        bu = float(b @ u)
        uu = float(u @ u)
        coef = bu / uu
        proj = coef * u
        residual = b - proj

        ax = self.ax
        ax.clear()
        ax.axhline(0, color="#999", lw=0.5); ax.axvline(0, color="#999", lw=0.5)
        ax.grid(alpha=0.25)

        # Span line
        t_line = np.linspace(-3, 3, 2)
        line = np.outer(t_line, u)
        ax.plot(line[:, 0], line[:, 1], "--", color="#aaa", lw=1.2, label="span(u)")

        ax.quiver(0, 0, b[0], b[1], angles="xy", scale_units="xy", scale=1, color="C3",
                  width=0.012, label="b (target)")
        ax.quiver(0, 0, u[0], u[1], angles="xy", scale_units="xy", scale=1, color="C0",
                  width=0.012, label="u (direction)")
        ax.quiver(0, 0, proj[0], proj[1], angles="xy", scale_units="xy", scale=1, color="green",
                  width=0.012, label="proj_u(b)")
        # Residual segment from b to proj
        ax.plot([b[0], proj[0]], [b[1], proj[1]], "--", color="purple", lw=1.5, label="residual r = b − proj")

        ax.set_xlim(-6, 6); ax.set_ylim(-6, 6); ax.set_aspect("equal")
        ax.set_title("Projection of b onto span(u)")
        ax.legend(loc="upper left", fontsize=9)
        self.canvas.draw_idle()

        self.calc.configure(
            text=(
                f"b · u = ({b[0]:.2f})({u[0]:.2f}) + ({b[1]:.2f})({u[1]:.2f}) = {bu:+.4f}\n"
                f"u · u = ({u[0]:.2f})² + ({u[1]:.2f})² = {uu:.4f}\n"
                f"proj_u(b) = (b·u / u·u) · u = ({bu:.4f}/{uu:.4f}) · u = "
                f"{coef:+.4f} · u = ({proj[0]:+.4f}, {proj[1]:+.4f})\n"
                f"residual r = b − proj = ({residual[0]:+.4f}, {residual[1]:+.4f})    "
                f"r · u = {float(residual @ u):+.6f} ≈ 0  (residual is orthogonal to u)"
            )
        )
