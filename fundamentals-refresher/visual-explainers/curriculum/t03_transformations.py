from __future__ import annotations

import tkinter as tk

from curriculum.base import TopicFrame
from modules.practice import determinant_problem
from views.transformations_view import TransformationsDemo


class LinearTransformationsTopic(TopicFrame):
    TITLE = "Linear transformations"
    BUILDS_ON = "matrix multiplication (a transform is just M·v for every v)"
    OVERVIEW = (
        "A matrix is a function: it takes a vector in and gives a vector out, linearly "
        "(scales and rotates space, no bending). The determinant tells you how the "
        "transformation rescales area / volume; its sign tells you whether orientation flips. "
        "A neural-net layer is a linear transform followed by a nonlinearity."
    )

    def build_demo(self, parent: tk.Misc) -> None:
        TransformationsDemo(parent).pack(fill="both", expand=True)

    def build_practice(self, parent: tk.Misc) -> None:
        self.add_practice(parent, determinant_problem)
