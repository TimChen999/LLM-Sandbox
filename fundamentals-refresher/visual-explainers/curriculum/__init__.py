"""Curriculum: ordered list of topics for the linear-algebra refresher."""
from __future__ import annotations

from curriculum.t01_vectors import VectorsTopic
from curriculum.t02_matrix_mult import MatrixMultTopic
from curriculum.t03_transformations import LinearTransformationsTopic
from curriculum.t04_rank import RankNullspaceTopic
from curriculum.t05_eigenvectors import EigenvectorsTopic
from curriculum.t06_svd import SVDTopic
from curriculum.t07_projections import ProjectionsTopic
from curriculum.t08_psd import PSDTopic
from curriculum.t09_matrix_calculus import MatrixCalculusTopic
from curriculum.t10_factorizations import FactorizationsTopic

TOPICS: list[type] = [
    VectorsTopic,
    MatrixMultTopic,
    LinearTransformationsTopic,
    RankNullspaceTopic,
    EigenvectorsTopic,
    SVDTopic,
    ProjectionsTopic,
    PSDTopic,
    MatrixCalculusTopic,
    FactorizationsTopic,
]
