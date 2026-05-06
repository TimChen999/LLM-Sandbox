from __future__ import annotations

import tkinter as tk

from curriculum.base import TopicFrame
from modules.practice import matrix_cell_problem
from views.matrix_mult_view import MatrixMultView


class MatrixMultTopic(TopicFrame):
    TITLE = "Matrix multiplication"
    BUILDS_ON = "dot products (each cell C[i,j] is one)"
    OVERVIEW = (
        "Matrix multiplication packs many dot products into one operation: C[i,j] is the "
        "dot product of row i of A with column j of B. Every neural-network forward pass, "
        "every batched linear transform, every covariance — they're all matrix products."
    )

    def build_demo(self, parent: tk.Misc) -> None:
        MatrixMultView(parent).pack(fill="both", expand=True)

    def build_practice(self, parent: tk.Misc) -> None:
        self.add_practice(parent, matrix_cell_problem)
