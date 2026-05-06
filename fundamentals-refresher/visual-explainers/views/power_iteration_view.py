"""Power-iteration eigenvector animation."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from modules.linear_algebra import power_iteration, power_iteration_trajectory
from views._helpers import LabeledSlider


class PowerIterationView(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)

        self.a11 = tk.DoubleVar(value=2.0)
        self.a12 = tk.DoubleVar(value=1.0)
        self.a21 = tk.DoubleVar(value=1.0)
        self.a22 = tk.DoubleVar(value=2.0)
        self.max_iters = tk.IntVar(value=20)
        self.speed_ms = tk.IntVar(value=300)

        self.iter_idx = 0
        self.playing = False
        self._after_id: str | None = None

        self._build_controls()
        self._build_plot()
        self._recompute()

    # ----- UI -----
    def _build_controls(self) -> None:
        bar = ttk.Frame(self, padding=(8, 8))
        bar.pack(side="top", fill="x")

        for label, var in [
            ("A[0,0]", self.a11),
            ("A[0,1]", self.a12),
            ("A[1,0]", self.a21),
            ("A[1,1]", self.a22),
        ]:
            LabeledSlider(
                bar, label, var, -3.0, 3.0, length=120,
                command=lambda *_: self._recompute(),
            ).pack(side="left", padx=6)

        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=8)

        self.play_btn = ttk.Button(bar, text="▶ Play", command=self._toggle_play)
        self.play_btn.pack(side="left", padx=2)
        ttk.Button(bar, text="⏮ Reset", command=self._reset).pack(side="left", padx=2)

        ttk.Label(bar, text="max iters:").pack(side="left", padx=(12, 4))
        ttk.Spinbox(
            bar, from_=1, to=100, textvariable=self.max_iters, width=4, command=self._recompute
        ).pack(side="left")
        LabeledSlider(
            bar, "speed (ms)", self.speed_ms, 50, 800, length=140, fmt="{:.0f}",
        ).pack(side="left", padx=(12, 0))

    def _build_plot(self) -> None:
        # Pack the status panel FIRST (side="bottom") so it's not squeezed by the
        # canvas (packed next with expand=True).
        status_frame = ttk.Frame(self, relief="groove", borderwidth=2, padding=(12, 8))
        status_frame.pack(side="bottom", fill="x")
        ttk.Label(
            status_frame, text="Current state", font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")
        self.status = ttk.Label(
            status_frame,
            text="",
            font=("Consolas", 12),
            justify="left",
            anchor="w",
        )
        self.status.pack(fill="x", pady=(4, 0))

        self.fig = Figure(figsize=(11, 4.2), tight_layout=True)
        self.ax_main = self.fig.add_subplot(1, 2, 1)
        self.ax_conv = self.fig.add_subplot(1, 2, 2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ----- state -----
    def _recompute(self) -> None:
        self._stop()
        self.A = np.array(
            [[self.a11.get(), self.a12.get()], [self.a21.get(), self.a22.get()]]
        )
        n = int(self.max_iters.get())
        v0 = np.array([1.0, 0.0])
        self.traj = power_iteration_trajectory(self.A, v0, n)
        try:
            eig, vec = power_iteration(self.A, n_iter=500)
            self.dom_val = eig
            self.dom_vec = vec
        except Exception:
            self.dom_val, self.dom_vec = float("nan"), np.array([np.nan, np.nan])
        self.iter_idx = 0
        self._redraw()

    def _reset(self) -> None:
        self._stop()
        self.iter_idx = 0
        self._redraw()

    def _toggle_play(self) -> None:
        if self.playing:
            self._stop()
        else:
            self._play()

    def _play(self) -> None:
        if self.iter_idx >= len(self.traj) - 1:
            self.iter_idx = 0
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
        if self.iter_idx >= len(self.traj) - 1:
            self._stop()
            return
        self.iter_idx += 1
        self._redraw()
        self._after_id = self.after(self.speed_ms.get(), self._tick)

    # ----- drawing -----
    def _redraw(self) -> None:
        ax = self.ax_main
        ax.clear()
        theta = np.linspace(0, 2 * np.pi, 200)
        ax.plot(np.cos(theta), np.sin(theta), "k--", alpha=0.3, label="unit circle")
        if len(self.traj) > 0:
            seen = self.traj[: self.iter_idx + 1]
            ax.plot(seen[:, 0], seen[:, 1], "o-", color="C0", alpha=0.4, label="iterates")
            cur = self.traj[self.iter_idx]
            ax.quiver(
                0,
                0,
                cur[0],
                cur[1],
                angles="xy",
                scale_units="xy",
                scale=1,
                color="C0",
                width=0.012,
            )
        if not np.isnan(self.dom_vec).any():
            ax.quiver(
                0,
                0,
                self.dom_vec[0],
                self.dom_vec[1],
                angles="xy",
                scale_units="xy",
                scale=1,
                color="green",
                alpha=0.5,
                width=0.012,
            )
            ax.quiver(
                0,
                0,
                -self.dom_vec[0],
                -self.dom_vec[1],
                angles="xy",
                scale_units="xy",
                scale=1,
                color="green",
                alpha=0.2,
                width=0.012,
            )
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.6, 1.6)
        ax.set_aspect("equal")
        ax.grid(alpha=0.3)
        ax.set_title(f"Iterate vs. dominant eigenvector  (step {self.iter_idx}/{len(self.traj) - 1})")
        ax.legend(loc="upper left", fontsize=9)

        # convergence plot: distance between consecutive iterates
        ax2 = self.ax_conv
        ax2.clear()
        if len(self.traj) > 1:
            diffs = np.linalg.norm(np.diff(self.traj, axis=0), axis=1)
            shown = diffs[: self.iter_idx]
            ax2.semilogy(np.arange(1, len(shown) + 1), shown, "o-", color="C1")
            ax2.semilogy(
                np.arange(1, len(diffs) + 1),
                diffs,
                "o-",
                color="C1",
                alpha=0.15,
            )
            ax2.set_title("‖vₙ − vₙ₋₁‖   (log scale)")
            ax2.set_xlabel("iteration")
            ax2.grid(alpha=0.3, which="both")

        self.canvas.draw_idle()

        n = self.iter_idx
        if len(self.traj) > 0 and n + 1 < len(self.traj):
            v = self.traj[n]
            Av = self.A @ v
            norm = float(np.linalg.norm(Av))
            v_next = Av / norm if norm > 0 else Av
            rayleigh = float(v_next @ self.A @ v_next)
            np_vals = sorted(np.linalg.eigvals(self.A).real, reverse=True)
            lines = [
                f"v_{n}       = ({v[0]:+.4f}, {v[1]:+.4f})",
                f"A · v_{n}   = ({Av[0]:+.4f}, {Av[1]:+.4f})",
                f"‖A · v_{n}‖ = {norm:.4f}",
                f"v_{n + 1}     = A·v_{n} / ‖A·v_{n}‖ = ({v_next[0]:+.4f}, {v_next[1]:+.4f})",
                f"Rayleigh quotient  v_{n + 1}ᵀ A v_{n + 1} ≈ {rayleigh:+.4f}    (numpy eigenvalues: {[round(v, 4) for v in np_vals]})",
            ]
            self.status.configure(text="\n".join(lines))
        else:
            v = self.traj[n] if len(self.traj) > 0 else np.array([np.nan, np.nan])
            np_vals = sorted(np.linalg.eigvals(self.A).real, reverse=True)
            self.status.configure(
                text=(
                    f"v_{n} = ({v[0]:+.4f}, {v[1]:+.4f})    converged.\n"
                    f"Dominant eigenvalue ≈ {self.dom_val:+.4f}    "
                    f"(numpy eigenvalues: {[round(v, 4) for v in np_vals]})"
                )
            )
