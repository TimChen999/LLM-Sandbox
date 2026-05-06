"""Matrix factorizations — show A and its QR / LU / Cholesky decomposition."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import numpy as np
import scipy.linalg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class FactorizationsDemo(ttk.Frame):
    METHODS = ("QR", "LU", "Cholesky")

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.method = tk.StringVar(value="QR")
        self.seed = tk.IntVar(value=0)
        self._build_controls()
        self._build_plot()
        self._recompute()

    def _build_controls(self) -> None:
        bar = ttk.Frame(self, padding=(8, 8))
        bar.pack(side="top", fill="x")
        ttk.Label(bar, text="Method:").pack(side="left", padx=(0, 4))
        for m in self.METHODS:
            ttk.Radiobutton(bar, text=m, value=m, variable=self.method,
                            command=self._recompute).pack(side="left", padx=4)
        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=12)
        ttk.Label(bar, text="seed:").pack(side="left", padx=(0, 4))
        ttk.Spinbox(bar, from_=0, to=999, textvariable=self.seed, width=5,
                    command=self._recompute).pack(side="left")
        ttk.Button(bar, text="🎲 New matrix", command=self._new_seed).pack(side="left", padx=8)

    def _new_seed(self) -> None:
        self.seed.set((self.seed.get() + 1) % 1000)
        self._recompute()

    def _build_plot(self) -> None:
        derivation = ttk.LabelFrame(self, text="  Calculation  ", padding=(12, 8))
        derivation.pack(side="bottom", fill="x")
        self.calc = ttk.Label(derivation, text="", font=("Consolas", 11), justify="left", anchor="w")
        self.calc.pack(fill="x")

        self.fig = Figure(figsize=(11, 4.5), tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _recompute(self) -> None:
        rng = np.random.default_rng(int(self.seed.get()))
        method = self.method.get()
        if method == "Cholesky":
            L_true = np.tril(rng.standard_normal((3, 3)))
            for i in range(3):
                if abs(L_true[i, i]) < 0.5:
                    L_true[i, i] = 1.0 if L_true[i, i] >= 0 else -1.0
            A = L_true @ L_true.T
            L = np.linalg.cholesky(A)
            self._draw_three(["A (PSD)", "L (lower)", "Lᵀ"], [A, L, L.T])
            verify = np.allclose(A, L @ L.T)
            self.calc.configure(
                text=(
                    f"Cholesky:  A = L Lᵀ   (only for symmetric PSD A)\n"
                    f"L is lower triangular with positive diagonal.\n"
                    f"Verify L Lᵀ = A:  {verify}    (used in solving normal equations efficiently)"
                )
            )
        elif method == "LU":
            A = rng.standard_normal((3, 3))
            P, L, U = scipy.linalg.lu(A)
            self._draw_three(["A", "L (unit lower tri)", "U (upper tri)"], [A, L, U])
            verify = np.allclose(P @ L @ U, A)
            self.calc.configure(
                text=(
                    f"LU (with row pivoting):  P A = L U\n"
                    f"L is unit-diagonal lower triangular; U is upper triangular.\n"
                    f"Used to solve A x = b in O(n³) once, then O(n²) per right-hand side. "
                    f"Verify  P L U = A: {verify}"
                )
            )
        else:  # QR
            A = rng.standard_normal((3, 3))
            Q, R = np.linalg.qr(A)
            self._draw_three(["A", "Q (orthogonal)", "R (upper tri)"], [A, Q, R])
            ortho = np.allclose(Q.T @ Q, np.eye(3), atol=1e-9)
            verify = np.allclose(Q @ R, A)
            self.calc.configure(
                text=(
                    f"QR:  A = Q R\n"
                    f"Q is orthogonal (QᵀQ = I, verified: {ortho}); R is upper triangular.\n"
                    f"Used in least-squares: A x = b  →  R x = Qᵀ b. Verify Q R = A: {verify}"
                )
            )

    def _draw_three(self, titles, mats) -> None:
        self.fig.clear()
        for k, (title, M) in enumerate(zip(titles, mats), start=1):
            ax = self.fig.add_subplot(1, 3, k)
            vmax = max(1.0, float(np.max(np.abs(M))))
            ax.imshow(M, cmap="RdBu_r", vmin=-vmax, vmax=vmax, alpha=0.6)
            for i in range(M.shape[0]):
                for j in range(M.shape[1]):
                    ax.text(j, i, f"{M[i, j]:+.2f}", ha="center", va="center", fontsize=10)
            ax.set_title(title)
            ax.set_xticks([]); ax.set_yticks([])
        self.canvas.draw_idle()
