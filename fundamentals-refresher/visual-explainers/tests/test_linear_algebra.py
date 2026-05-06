"""Tests for modules.linear_algebra.

Strategy:
- Known-answer tests for hand-computable cases.
- Cross-check tests against numpy for randomly generated inputs.
- Property tests for invariants (e.g., consistency between functions).
"""
import numpy as np
import pytest

from modules.linear_algebra import (
    matrix_multiply_steps,
    power_iteration,
    power_iteration_trajectory,
    transformation_path,
)


# ----- matrix_multiply_steps -----

def test_matrix_multiply_steps_known_2x2():
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    B = np.array([[5.0, 6.0], [7.0, 8.0]])
    cells = list(matrix_multiply_steps(A, B))
    assert len(cells) == 4
    cell_values = {(i, j): v for i, j, _, _, v in cells}
    # A @ B = [[19, 22], [43, 50]]
    assert cell_values == {(0, 0): 19, (0, 1): 22, (1, 0): 43, (1, 1): 50}


def test_matrix_multiply_steps_matches_numpy_random():
    rng = np.random.default_rng(0)
    for _ in range(10):
        m, k, n = rng.integers(1, 6, size=3)
        A = rng.standard_normal((m, k))
        B = rng.standard_normal((k, n))
        expected = A @ B
        got = np.zeros_like(expected)
        for i, j, row, col, v in matrix_multiply_steps(A, B):
            got[i, j] = v
            # also check the row/col returned are consistent with the value
            assert np.isclose(row @ col, v)
        assert np.allclose(got, expected)


def test_matrix_multiply_steps_shape_mismatch_raises():
    with pytest.raises(ValueError):
        list(matrix_multiply_steps(np.zeros((2, 3)), np.zeros((4, 2))))


# ----- power_iteration -----

def test_power_iteration_known_2x2():
    # eigenvalues 1 and 3; dominant is 3 with eigenvector (1, 1)/sqrt(2)
    A = np.array([[2.0, 1.0], [1.0, 2.0]])
    eig, vec = power_iteration(A)
    assert eig == pytest.approx(3.0, abs=1e-6)
    expected = np.array([1.0, 1.0]) / np.sqrt(2)
    assert np.allclose(vec, expected, atol=1e-6)


def test_power_iteration_diagonal():
    # diagonal: eigenvalues are the diagonal entries
    A = np.diag([5.0, -2.0, 1.0])
    eig, vec = power_iteration(A)
    assert eig == pytest.approx(5.0, abs=1e-6)
    # eigenvector should be the standard basis vector for the dominant entry
    assert np.allclose(np.abs(vec), [1.0, 0.0, 0.0], atol=1e-6)


def test_power_iteration_matches_numpy_for_symmetric():
    rng = np.random.default_rng(42)
    for _ in range(20):
        Q, _ = np.linalg.qr(rng.standard_normal((5, 5)))
        # well-separated eigenvalues so power iteration converges fast
        diag = np.diag([5.0, 4.0, 3.0, 2.0, 1.0])
        A = Q @ diag @ Q.T
        eig, vec = power_iteration(A, n_iter=500)
        np_vals, np_vecs = np.linalg.eigh(A)
        # eigh returns ascending order; dominant is last
        assert eig == pytest.approx(np_vals[-1], abs=1e-4)
        np_vec = np_vecs[:, -1]
        # eigenvectors are unique up to sign
        assert np.allclose(vec, np_vec, atol=1e-3) or np.allclose(
            vec, -np_vec, atol=1e-3
        )


def test_power_iteration_eigenvector_is_unit_length():
    rng = np.random.default_rng(1)
    A = rng.standard_normal((4, 4))
    A = A + A.T  # make symmetric so a real dominant eigenvector exists
    _, vec = power_iteration(A)
    assert np.linalg.norm(vec) == pytest.approx(1.0, abs=1e-9)


# ----- power_iteration_trajectory -----

def test_trajectory_first_point_is_normalized_v0():
    A = np.eye(3)
    v0 = np.array([2.0, 0.0, 0.0])
    traj = power_iteration_trajectory(A, v0, n_iter=5)
    assert np.allclose(traj[0], np.array([1.0, 0.0, 0.0]))


def test_trajectory_all_points_unit_length():
    rng = np.random.default_rng(3)
    A = rng.standard_normal((3, 3))
    A = A + A.T
    v0 = rng.standard_normal(3)
    traj = power_iteration_trajectory(A, v0, n_iter=20)
    norms = np.linalg.norm(traj, axis=1)
    assert np.allclose(norms, 1.0)


def test_trajectory_converges_to_dominant_eigenvector():
    A = np.array([[2.0, 1.0], [1.0, 2.0]])
    v0 = np.array([1.0, 0.0])
    traj = power_iteration_trajectory(A, v0, n_iter=50)
    expected = np.array([1.0, 1.0]) / np.sqrt(2)
    final = traj[-1]
    # may converge to either sign
    assert np.allclose(final, expected, atol=1e-4) or np.allclose(
        final, -expected, atol=1e-4
    )


# ----- transformation_path -----

def test_transformation_path_shapes():
    A = np.array([[2.0, 0.0], [0.0, 0.5]])
    circle, transformed = transformation_path(A, n_points=50)
    assert circle.shape == (2, 50)
    assert transformed.shape == (2, 50)


def test_transformation_path_circle_is_unit_circle():
    circle, _ = transformation_path(np.eye(2), n_points=100)
    norms = np.linalg.norm(circle, axis=0)
    assert np.allclose(norms, 1.0)


def test_transformation_path_consistent_with_matmul():
    rng = np.random.default_rng(7)
    A = rng.standard_normal((2, 2))
    circle, transformed = transformation_path(A, n_points=20)
    assert np.allclose(transformed, A @ circle)


def test_transformation_path_rejects_non_2x2():
    with pytest.raises(ValueError):
        transformation_path(np.eye(3))
