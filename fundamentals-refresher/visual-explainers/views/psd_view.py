"""Positive (semi)definite matrices — contour of the quadratic form xᵀAx."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class PSDDemo(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.a11 = tk.DoubleVar(value=2.0)
        self.a22 = tk.DoubleVar(value=1.0)
        self.a12 = tk.DoubleVar(value=0.5)  # off-diagonal (symmetric: a21 = a12)
        self._build_controls()
        self._build_plot()
        self._recompute()

    def _build_controls(self) -> None:
        bar = ttk.Frame(self, padding=(8, 8))
        bar.pack(side="top", fill="x")
        for label, var in [("A[0,0]", self.a11), ("A[1,1]", self.a22), ("A[0,1]=A[1,0]", self.a12)]:
            box = ttk.Frame(bar)
            ttk.Label(box, text=label).pack()
            ttk.Scale(box, from_=-3, to=3, variable=var, orient="horizontal", length=140,
                      command=lambda *_: self._recompute()).pack()
            box.pack(side="left", padx=8)
        ttk.Button(bar, text="Make PSD (random Lᵀ L)", command=self._make_psd).pack(side="left", padx=8)

    def _make_psd(self) -> None:
        rng = np.random.default_rng()
        L = rng.standard_normal((2, 2))
        M = L.T @ L
        self.a11.set(float(M[0, 0])); self.a22.set(float(M[1, 1])); self.a12.set(float(M[0, 1]))
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
        a, c, b = self.a11.get(), self.a22.get(), self.a12.get()
        A = np.array([[a, b], [b, c]])
        eigs = np.sort(np.linalg.eigvalsh(A))
        psd = bool(np.all(eigs >= -1e-9))
        pd = bool(np.all(eigs > 1e-9))

        # Compute f(x) = xᵀ A x on a grid
        n = 200
        xs = np.linspace(-3, 3, n)
        X, Y = np.meshgrid(xs, xs)
        F = a * X**2 + 2 * b * X * Y + c * Y**2

        ax = self.ax
        ax.clear()
        cs = ax.contourf(X, Y, F, levels=20, cmap="RdBu_r")
        ax.contour(X, Y, F, levels=[0], colors="black", linewidths=1)
        # Eigen-axes
        evals, evecs = np.linalg.eigh(A)
        for k in range(2):
            v = evecs[:, k] * 2.5
            ax.plot([-v[0], v[0]], [-v[1], v[1]], color="green", lw=1.2, alpha=0.6)
            ax.text(v[0], v[1], f"λ={evals[k]:.2f}", color="green", fontsize=9)
        ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect("equal")
        verdict = "Positive definite" if pd else ("Positive semi-definite" if psd else "Indefinite")
        ax.set_title(f"f(x) = xᵀ A x   —   {verdict}")
        self.canvas.draw_idle()

        self.calc.configure(
            text=(
                f"A is symmetric:  A = [[{a:.2f}, {b:.2f}], [{b:.2f}, {c:.2f}]]\n"
                f"f(x, y) = {a:.2f}·x² + {2*b:.2f}·x·y + {c:.2f}·y²\n"
                f"eigenvalues of A: ({eigs[0]:+.4f}, {eigs[1]:+.4f})\n"
                f"trace = {a+c:+.4f},  det = {a*c - b*b:+.4f}\n"
                f"{'PSD' if psd else 'NOT PSD'} — "
                f"{'all eigenvalues ≥ 0; level sets of f are ellipses (or degenerate).' if psd else 'one eigenvalue is negative; level sets are hyperbolas — saddle.'}"
            )
        )
