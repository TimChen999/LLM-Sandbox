from __future__ import annotations

import tkinter as tk

from curriculum.base import TopicFrame
from modules.practice import dot_product_problem
from views.vectors_view import VectorsDemo


class VectorsTopic(TopicFrame):
    TITLE = "Vectors, dot products, norms"
    BUILDS_ON = "(start of curriculum)"
    OVERVIEW = (
        "Vectors are points / arrows in ℝⁿ. The dot product a·b measures alignment; "
        "norms ‖v‖ measure size. These are the most-used operations in ML — every "
        "similarity metric, every loss term, every regularizer is built on them."
    )

    def build_demo(self, parent: tk.Misc) -> None:
        VectorsDemo(parent).pack(fill="both", expand=True)

    def build_practice(self, parent: tk.Misc) -> None:
        self.add_practice(parent, dot_product_problem)
