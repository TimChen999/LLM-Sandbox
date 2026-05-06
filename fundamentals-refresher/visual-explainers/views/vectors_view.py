"""Vectors / dot products / norms — interactive 2D plot of two vectors."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from views._helpers import LabeledSlider


class VectorsDemo(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.ax_var = tk.DoubleVar(value=3.0)
        self.ay_var = tk.DoubleVar(value=1.0)
        self.bx_var = tk.DoubleVar(value=1.0)
        self.by_var = tk.DoubleVar(value=2.0)
        self._build_controls()
        self._build_plot()
        self._recompute()

    def _build_controls(self) -> None:
        bar = ttk.Frame(self, padding=(8, 8))
        bar.pack(side="top", fill="x")
        for label, var in [
            ("a.x", self.ax_var),
            ("a.y", self.ay_var),
            ("b.x", self.bx_var),
            ("b.y", self.by_var),
        ]:
            LabeledSlider(
                bar, label, var, -5, 5, length=150,
                command=lambda *_: self._recompute(),
            ).pack(side="left", padx=10)

    def _build_plot(self) -> None:
        derivation = ttk.LabelFrame(self, text="  Calculation  ", padding=(12, 8))
        derivation.pack(side="bottom", fill="x")
        self.calc = ttk.Label(
            derivation, text="", font=("Consolas", 11), justify="left", anchor="w"
        )
        self.calc.pack(fill="x")

        self.fig = Figure(figsize=(7, 6), tight_layout=True)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _recompute(self) -> None:
        a = np.array([self.ax_var.get(), self.ay_var.get()])
        b = np.array([self.bx_var.get(), self.by_var.get()])
        self._draw(a, b)

    def _draw(self, a: np.ndarray, b: np.ndarray) -> None:
        ax = self.ax
        ax.clear()
        ax.axhline(0, color="#999", lw=0.5)
        ax.axvline(0, color="#999", lw=0.5)
        ax.grid(alpha=0.25)

        ax.quiver(0, 0, a[0], a[1], angles="xy", scale_units="xy", scale=1, color="C0", width=0.012)
        ax.quiver(0, 0, b[0], b[1], angles="xy", scale_units="xy", scale=1, color="C3", width=0.012)
        ax.text(a[0] * 1.05, a[1] * 1.05, "a", color="C0", fontsize=14, fontweight="bold")
        ax.text(b[0] * 1.05, b[1] * 1.05, "b", color="C3", fontsize=14, fontweight="bold")

        # projection of a onto b (if b nonzero) — placed off to the side to avoid b's label
        if np.linalg.norm(b) > 1e-9:
            t = (a @ b) / (b @ b)
            p = t * b
            ax.plot([a[0], p[0]], [a[1], p[1]], "--", color="#888", lw=1.2)
            ax.quiver(
                0, 0, p[0], p[1],
                angles="xy", scale_units="xy", scale=1, color="#888",
                width=0.008, alpha=0.7,
            )
            b_unit = b / np.linalg.norm(b)
            perp = np.array([-b_unit[1], b_unit[0]]) * 0.5
            ax.annotate(
                "proj_b(a)",
                xy=(p[0], p[1]),
                xytext=(p[0] + perp[0], p[1] + perp[1]),
                color="#555", fontsize=9,
                arrowprops=dict(arrowstyle="-", color="#aaa", lw=0.8),
            )

        ax.set_xlim(-7, 7)
        ax.set_ylim(-7, 7)
        ax.set_aspect("equal")
        ax.set_title("Two vectors a and b — drag the sliders to move them")
        self.canvas.draw_idle()

        dot = float(a @ b)
        l1a, l2a, linfa = float(np.sum(np.abs(a))), float(np.linalg.norm(a)), float(np.max(np.abs(a)))
        l1b, l2b, linfb = float(np.sum(np.abs(b))), float(np.linalg.norm(b)), float(np.max(np.abs(b)))
        cos = dot / (l2a * l2b) if l2a * l2b > 1e-9 else float("nan")
        angle_deg = float(np.degrees(np.arccos(np.clip(cos, -1.0, 1.0)))) if not np.isnan(cos) else float("nan")

        self.calc.configure(
            text=(
                f"a · b = ({a[0]:.2f})({b[0]:.2f}) + ({a[1]:.2f})({b[1]:.2f}) = {dot:+.4f}\n"
                f"||a||₁={l1a:.3f}  ||a||₂={l2a:.3f}  ||a||∞={linfa:.3f}    "
                f"||b||₁={l1b:.3f}  ||b||₂={l2b:.3f}  ||b||∞={linfb:.3f}\n"
                f"cos∠(a,b) = (a·b) / (||a||₂ ||b||₂) = {cos:+.4f}    →    angle ≈ {angle_deg:.1f}°"
            )
        )
