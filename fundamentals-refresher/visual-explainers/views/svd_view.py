"""SVD — animate the unit circle through V^T → Σ → U as A = U Σ V^T."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from views._helpers import LabeledSlider


class SVDDemo(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.a11 = tk.DoubleVar(value=2.0)
        self.a12 = tk.DoubleVar(value=1.0)
        self.a21 = tk.DoubleVar(value=0.0)
        self.a22 = tk.DoubleVar(value=1.5)
        self.t = tk.DoubleVar(value=3.0)  # 0..3, stages: 0=input, 1=after Vᵀ, 2=after Σ, 3=after U
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
            LabeledSlider(
                bar, label, var, -3, 3, length=120,
                command=lambda *_: self._recompute(),
            ).pack(side="left", padx=6)

        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=8)
        ttk.Button(bar, text="▶ Animate Vᵀ → Σ → U", command=self._animate).pack(side="left", padx=4)

        LabeledSlider(
            bar, "stage  (0=in · 1=Vᵀ · 2=Σ · 3=U)", self.t, 0, 3, length=240,
            command=lambda *_: self._redraw(), fmt="{:.2f}",
        ).pack(side="left", padx=(12, 4))

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
        self._cancel_animation()
        self._redraw()

    def _animate(self) -> None:
        self._cancel_animation()
        self._anim_step = 0
        self._anim_total = 90
        self._tick()

    def _tick(self) -> None:
        if self._anim_step > self._anim_total:
            return
        self.t.set(3.0 * self._anim_step / self._anim_total)
        self._redraw()
        self._anim_step += 1
        self._after_id = self.after(40, self._tick)

    def _cancel_animation(self) -> None:
        if self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None

    def _redraw(self) -> None:
        A = np.array([[self.a11.get(), self.a12.get()],
                      [self.a21.get(), self.a22.get()]])
        try:
            U, s, Vt = np.linalg.svd(A)
        except np.linalg.LinAlgError:
            return
        Sigma = np.diag(s)
        t = float(self.t.get())

        # Apply stages with interpolation
        # stage 0->1: identity → V^T
        # stage 1->2: V^T → Σ V^T
        # stage 2->3: Σ V^T → U Σ V^T = A
        if t <= 1:
            M = (1 - t) * np.eye(2) + t * Vt
            stage_label = f"After Vᵀ (rotation)  — interp {t:.2f}"
        elif t <= 2:
            tt = t - 1
            M = (1 - tt) * Vt + tt * (Sigma @ Vt)
            stage_label = f"After Σ (axis-aligned scale)  — interp {tt:.2f}"
        else:
            tt = t - 2
            M = (1 - tt) * (Sigma @ Vt) + tt * (U @ Sigma @ Vt)
            stage_label = f"After U (rotation)  — interp {tt:.2f}"

        theta = np.linspace(0, 2 * np.pi, 200)
        circle = np.vstack([np.cos(theta), np.sin(theta)])
        transformed = M @ circle

        ax = self.ax
        ax.clear()
        ax.axhline(0, color="#999", lw=0.5); ax.axvline(0, color="#999", lw=0.5)
        ax.grid(alpha=0.25)
        ax.plot(circle[0], circle[1], "k--", alpha=0.3, label="unit circle")
        ax.plot(transformed[0], transformed[1], color="C0", lw=2, label="image")
        # Singular axes (final positions)
        for k in range(2):
            v = U[:, k] * s[k]
            ax.quiver(0, 0, v[0], v[1], angles="xy", scale_units="xy", scale=1,
                      color="green", alpha=0.4, width=0.01)
        ax.set_xlim(-4, 4); ax.set_ylim(-4, 4); ax.set_aspect("equal")
        ax.set_title(stage_label)
        ax.legend(loc="upper left", fontsize=9)
        self.canvas.draw_idle()

        self.calc.configure(
            text=(
                f"SVD:  A = U Σ Vᵀ\n"
                f"σ₁ = {s[0]:.4f}    σ₂ = {s[1]:.4f}    "
                f"(σᵢ are eigenvalues' square roots of AᵀA — connecting back to the previous topic)\n"
                f"U =  [[{U[0,0]:+.3f}, {U[0,1]:+.3f}], [{U[1,0]:+.3f}, {U[1,1]:+.3f}]]    "
                f"Vᵀ = [[{Vt[0,0]:+.3f}, {Vt[0,1]:+.3f}], [{Vt[1,0]:+.3f}, {Vt[1,1]:+.3f}]]\n"
                f"Visually: a circle becomes an ellipse with semi-axes σ₁, σ₂ rotated by U."
            )
        )
