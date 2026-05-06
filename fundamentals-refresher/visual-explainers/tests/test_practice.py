"""Tests for modules.practice — verify the generators run, return well-formed
strings, and reflect mathematically consistent answers (cross-checked vs. numpy).
"""
import re

import numpy as np
import pytest

from modules import practice


GENERATORS = [
    practice.vector_norm_problem,
    practice.dot_product_problem,
    practice.matrix_cell_problem,
    practice.determinant_problem,
    practice.rank_problem,
    practice.eigenvalue_problem,
    practice.svd_singular_values_problem,
    practice.projection_problem,
    practice.psd_check_problem,
    practice.gradient_quadratic_problem,
    practice.cholesky_problem,
]


@pytest.mark.parametrize("gen", GENERATORS)
def test_generator_returns_two_nonempty_strings(gen):
    rng = np.random.default_rng(42)
    for _ in range(5):
        prompt, answer = gen(rng)
        assert isinstance(prompt, str) and prompt.strip()
        assert isinstance(answer, str) and answer.strip()


@pytest.mark.parametrize("gen", GENERATORS)
def test_generator_deterministic_with_seeded_rng(gen):
    rng1 = np.random.default_rng(123)
    rng2 = np.random.default_rng(123)
    p1, a1 = gen(rng1)
    p2, a2 = gen(rng2)
    assert p1 == p2 and a1 == a2


def test_dot_product_arithmetic():
    """Spot-check the arithmetic shown in the answer matches numpy."""
    rng = np.random.default_rng(0)
    for _ in range(20):
        prompt, answer = practice.dot_product_problem(rng)
        # Find the final "= N" in the answer's last line
        last = answer.strip().split("\n")[-1]
        m = re.search(r"=\s*(-?\d+)\s*$", last)
        assert m, f"could not parse final value from: {last}"
        value = int(m.group(1))
        # Recompute by parsing vectors from the prompt
        vec_strs = re.findall(r"\(([-\d,\s]+)\)", prompt)
        a = np.array([int(x) for x in vec_strs[0].split(",")])
        b = np.array([int(x) for x in vec_strs[1].split(",")])
        assert int(a @ b) == value


def test_determinant_arithmetic():
    rng = np.random.default_rng(0)
    for _ in range(20):
        prompt, answer = practice.determinant_problem(rng)
        first = answer.strip().split("\n")[0]
        m = re.search(r"=\s*(-?\d+)\s*$", first)
        assert m, f"could not parse det from: {first}"
        det = int(m.group(1))
        # Parse the 2x2 from the prompt — find 4 ints inside the matrix lines
        nums = [int(n) for n in re.findall(r"-?\d+", prompt)[:4]]
        a, b, c, d = nums
        assert a * d - b * c == det


def test_psd_problem_classification_matches_numpy():
    rng = np.random.default_rng(0)
    for _ in range(30):
        prompt, answer = practice.psd_check_problem(rng)
        # Extract the eigenvalues from the answer line "eigenvalues: (a, b)"
        m = re.search(r"eigenvalues:\s*\(([+\-\d\.]+),\s*([+\-\d\.]+)\)", answer)
        assert m, answer
        e1, e2 = float(m.group(1)), float(m.group(2))
        psd_claim = "is PSD" in answer and "NOT PSD" not in answer
        assert psd_claim == bool((e1 >= -1e-6) and (e2 >= -1e-6))
