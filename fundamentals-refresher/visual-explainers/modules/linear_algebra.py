"""Pure math functions for the linear algebra visual explainers.

Each function is testable against numpy. Visualization code lives in views/.
No plotting, no GUI imports here.
"""
from __future__ import annotations

from typing import Iterator

import numpy as np


def matrix_multiply_steps(
    A: np.ndarray, B: np.ndarray
) -> Iterator[tuple[int, int, np.ndarray, np.ndarray, float]]:
    """Yield each cell of A @ B as it would be computed, one at a time.

    Yields (i, j, row_i_of_A, col_j_of_B, dot_value).
    """
    if A.shape[1] != B.shape[0]:
        raise ValueError(
            f"shape mismatch: A has {A.shape[1]} cols, B has {B.shape[0]} rows"
        )
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            row = A[i, :]
            col = B[:, j]
            yield i, j, row, col, float(row @ col)


def power_iteration(
    A: np.ndarray, n_iter: int = 200, tol: float = 1e-10
) -> tuple[float, np.ndarray]:
    """Find the dominant eigenvalue/eigenvector of A via power iteration.

    Returns (eigenvalue, eigenvector). Eigenvector is unit length, with sign
    chosen so its largest-magnitude component is positive (canonical sign).
    """
    n = A.shape[0]
    v = np.ones(n) / np.sqrt(n)
    eigenvalue = 0.0
    for _ in range(n_iter):
        Av = A @ v
        norm = np.linalg.norm(Av)
        if norm < 1e-15:
            break
        new_v = Av / norm
        new_eigenvalue = float(new_v @ A @ new_v)  # Rayleigh quotient
        if np.linalg.norm(new_v - v) < tol or np.linalg.norm(new_v + v) < tol:
            v = new_v
            eigenvalue = new_eigenvalue
            break
        v = new_v
        eigenvalue = new_eigenvalue
    # canonical sign: largest |component| should be positive
    idx = int(np.argmax(np.abs(v)))
    if v[idx] < 0:
        v = -v
    return eigenvalue, v


def power_iteration_trajectory(
    A: np.ndarray, v0: np.ndarray, n_iter: int
) -> np.ndarray:
    """Return the sequence of normalized iterates v0, v1, ..., v_n.

    Shape: (n_iter + 1, len(v0)). Useful for visualizing convergence.
    """
    v = v0 / np.linalg.norm(v0)
    traj = [v.copy()]
    for _ in range(n_iter):
        Av = A @ v
        norm = np.linalg.norm(Av)
        if norm < 1e-15:
            break
        v = Av / norm
        traj.append(v.copy())
    return np.array(traj)


def transformation_path(
    A: np.ndarray, n_points: int = 200
) -> tuple[np.ndarray, np.ndarray]:
    """Return points on the unit circle and their image under a 2x2 matrix A.

    Returns (circle, transformed), each with shape (2, n_points).
    """
    if A.shape != (2, 2):
        raise ValueError("transformation_path expects a 2x2 matrix")
    theta = np.linspace(0, 2 * np.pi, n_points)
    circle = np.vstack([np.cos(theta), np.sin(theta)])
    transformed = A @ circle
    return circle, transformed
