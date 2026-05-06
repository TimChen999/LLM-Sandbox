from __future__ import annotations

import tkinter as tk

from curriculum.base import TopicFrame
from modules.practice import rank_problem
from views.rank_view import RankDemo


class RankNullspaceTopic(TopicFrame):
    TITLE = "Rank, null space, column space"
    BUILDS_ON = "linear transformations (rank = how much dimension survives)"
    OVERVIEW = (
        "The rank of a matrix is the dimension of its column space — i.e., how many "
        "independent directions its columns span. Low rank means redundancy: some "
        "columns are linear combinations of the others. PCA, low-rank approximation, "
        "LoRA, and recommender-system factorizations all exploit low rank."
    )

    def build_demo(self, parent: tk.Misc) -> None:
        RankDemo(parent).pack(fill="both", expand=True)

    def build_practice(self, parent: tk.Misc) -> None:
        self.add_practice(parent, rank_problem)
