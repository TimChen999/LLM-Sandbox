from __future__ import annotations

import tkinter as tk

from curriculum.base import TopicFrame
from modules.practice import psd_check_problem
from views.psd_view import PSDDemo


class PSDTopic(TopicFrame):
    TITLE = "Positive (semi)definite matrices"
    BUILDS_ON = "eigenvectors (M is PSD iff all eigenvalues ≥ 0)"
    OVERVIEW = (
        "A symmetric matrix M is positive semi-definite if vᵀM v ≥ 0 for all v — equivalently, "
        "all its eigenvalues are nonnegative. PSD matrices show up everywhere: every covariance "
        "matrix is PSD, the Hessian at a local minimum is PSD, kernel matrices in SVMs/GPs "
        "must be PSD. They guarantee well-defined geometry (ellipsoidal level sets, "
        "real-valued square roots via Cholesky)."
    )

    def build_demo(self, parent: tk.Misc) -> None:
        PSDDemo(parent).pack(fill="both", expand=True)

    def build_practice(self, parent: tk.Misc) -> None:
        self.add_practice(parent, psd_check_problem)
