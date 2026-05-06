from __future__ import annotations

import tkinter as tk

from curriculum.base import TopicFrame
from modules.practice import cholesky_problem
from views.factorizations_view import FactorizationsDemo


class FactorizationsTopic(TopicFrame):
    TITLE = "Matrix factorizations (QR, LU, Cholesky)"
    BUILDS_ON = "rank, PSD (Cholesky needs PSD; QR underlies stable least squares)"
    OVERVIEW = (
        "Factorizations rewrite a matrix as a product of structured ones (triangular, "
        "orthogonal). They're the engines under most numerical solvers: LU for general "
        "linear systems, QR for least squares (numerically stabler than the normal "
        "equations), Cholesky for PSD systems (twice as fast as LU). When you call "
        "numpy.linalg.solve, one of these is doing the work."
    )

    def build_demo(self, parent: tk.Misc) -> None:
        FactorizationsDemo(parent).pack(fill="both", expand=True)

    def build_practice(self, parent: tk.Misc) -> None:
        self.add_practice(parent, cholesky_problem)
