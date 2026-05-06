from __future__ import annotations

import tkinter as tk

from curriculum.base import TopicFrame
from modules.practice import svd_singular_values_problem
from views.svd_view import SVDDemo


class SVDTopic(TopicFrame):
    TITLE = "Singular Value Decomposition (SVD)"
    BUILDS_ON = "eigenvectors (σᵢ² are the eigenvalues of AᵀA)"
    OVERVIEW = (
        "SVD writes any matrix A = U Σ Vᵀ — geometrically, every linear transform is a "
        "rotation, then an axis-aligned scale, then another rotation. The singular values σᵢ "
        "tell you how much each axis is stretched. Truncating to the top-k σᵢ gives the "
        "best rank-k approximation (Eckart–Young), which is the engine behind PCA, "
        "low-rank compression, and LoRA fine-tuning."
    )

    def build_demo(self, parent: tk.Misc) -> None:
        SVDDemo(parent).pack(fill="both", expand=True)

    def build_practice(self, parent: tk.Misc) -> None:
        self.add_practice(parent, svd_singular_values_problem)
