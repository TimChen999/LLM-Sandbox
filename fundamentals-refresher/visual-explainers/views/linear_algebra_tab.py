"""Top-level Linear Algebra tab — contains sub-tabs for individual demos."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from views.matrix_mult_view import MatrixMultView
from views.power_iteration_view import PowerIterationView


class LinearAlgebraTab(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True)
        nb.add(MatrixMultView(nb), text="Matrix Multiplication")
        nb.add(PowerIterationView(nb), text="Power Iteration (Eigenvectors)")
