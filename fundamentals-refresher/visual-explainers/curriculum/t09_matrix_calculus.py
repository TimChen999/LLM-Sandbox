from __future__ import annotations

import tkinter as tk

from curriculum.base import TopicFrame
from modules.practice import gradient_quadratic_problem
from views.matrix_calculus_view import MatrixCalculusDemo


class MatrixCalculusTopic(TopicFrame):
    TITLE = "Matrix calculus (gradients, Jacobians, Hessians)"
    BUILDS_ON = "PSD matrices (the Hessian at an optimum tells you everything)"
    OVERVIEW = (
        "Matrix calculus is just chain rule with bookkeeping. The patterns you actually need "
        "in ML are short: ∇ₓ(aᵀx)=a, ∇ₓ(xᵀAx)=(A+Aᵀ)x (= 2Ax for symmetric A), "
        "and ∇_W(½‖Wx − y‖²) = (Wx − y)xᵀ. Backprop is just these rules applied "
        "left-to-right through a computation graph."
    )

    def build_demo(self, parent: tk.Misc) -> None:
        MatrixCalculusDemo(parent).pack(fill="both", expand=True)

    def build_practice(self, parent: tk.Misc) -> None:
        self.add_practice(parent, gradient_quadratic_problem)
