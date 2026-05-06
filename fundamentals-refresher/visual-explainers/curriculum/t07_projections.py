from __future__ import annotations

import tkinter as tk

from curriculum.base import TopicFrame
from modules.practice import projection_problem
from views.projections_view import ProjectionsDemo


class ProjectionsTopic(TopicFrame):
    TITLE = "Projections and least squares"
    BUILDS_ON = "vectors and dot products (projection is just a scaled u)"
    OVERVIEW = (
        "Projecting b onto a direction u finds the closest point in span(u) to b. "
        "Generalizing to a matrix A's column space gives the least-squares solution: "
        "the closed form x̂ = (AᵀA)⁻¹ Aᵀ b is exactly the projection of b onto col(A). "
        "Linear regression, PCA reconstructions, and beam-forming are all projections."
    )

    def build_demo(self, parent: tk.Misc) -> None:
        ProjectionsDemo(parent).pack(fill="both", expand=True)

    def build_practice(self, parent: tk.Misc) -> None:
        self.add_practice(parent, projection_problem)
