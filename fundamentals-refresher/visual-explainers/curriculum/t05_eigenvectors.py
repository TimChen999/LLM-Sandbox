from __future__ import annotations

import tkinter as tk

from curriculum.base import TopicFrame
from modules.practice import eigenvalue_problem
from views.power_iteration_view import PowerIterationView


class EigenvectorsTopic(TopicFrame):
    TITLE = "Eigenvalues and eigenvectors"
    BUILDS_ON = "linear transformations (eigenvectors are the directions A doesn't rotate)"
    OVERVIEW = (
        "An eigenvector v of A satisfies A·v = λ·v — A only stretches it by the scalar λ "
        "(the eigenvalue), without rotating its direction. Eigen-decomposition exposes the "
        "principal directions of a transformation. Power iteration is the simplest way to "
        "find the dominant one and underlies PageRank, PCA, and many spectral methods."
    )

    def build_demo(self, parent: tk.Misc) -> None:
        PowerIterationView(parent).pack(fill="both", expand=True)

    def build_practice(self, parent: tk.Misc) -> None:
        self.add_practice(parent, eigenvalue_problem)
