"""Random practice-problem generators, one per topic.

Each function takes a numpy Generator and returns (prompt, answer) — both strings
ready to display. The numeric work uses numpy/scipy so the answers are correct
by construction.
"""
from __future__ import annotations

import numpy as np

# ---------- formatting helpers ----------

def _fmt_matrix(M: np.ndarray, decimals: int = 0) -> str:
    rows = []
    for row in M:
        rows.append("  [ " + "  ".join(f"{v:>5.{decimals}f}" for v in row) + " ]")
    return "\n".join(rows)


def _fmt_vec(v: np.ndarray, decimals: int = 0) -> str:
    return "(" + ", ".join(f"{x:.{decimals}f}" for x in v) + ")"


# ---------- 01 vectors / norms ----------

def vector_norm_problem(rng: np.random.Generator) -> tuple[str, str]:
    n = rng.integers(2, 5)
    v = rng.integers(-6, 7, size=int(n))
    while np.all(v == 0):
        v = rng.integers(-6, 7, size=int(n))
    l1 = float(np.sum(np.abs(v)))
    l2 = float(np.linalg.norm(v))
    linf = float(np.max(np.abs(v)))
    prompt = (
        f"Compute the L1, L2, and L∞ norms of\n\n"
        f"   v = {_fmt_vec(v)}"
    )
    answer = (
        f"||v||₁ = sum |vᵢ| = {' + '.join(str(int(abs(x))) for x in v)} = {l1:.0f}\n"
        f"||v||₂ = sqrt(sum vᵢ²) = sqrt({sum(int(x)**2 for x in v)}) ≈ {l2:.4f}\n"
        f"||v||∞ = max |vᵢ| = {linf:.0f}"
    )
    return prompt, answer


def dot_product_problem(rng: np.random.Generator) -> tuple[str, str]:
    n = rng.integers(2, 5)
    a = rng.integers(-5, 6, size=int(n))
    b = rng.integers(-5, 6, size=int(n))
    dot = int(a @ b)
    terms = " + ".join(f"({int(x)})({int(y)})" for x, y in zip(a, b))
    products = " + ".join(f"{int(x*y)}" for x, y in zip(a, b))
    prompt = (
        f"Compute the dot product a · b for\n\n"
        f"   a = {_fmt_vec(a)}\n"
        f"   b = {_fmt_vec(b)}"
    )
    answer = (
        f"a · b = {terms}\n"
        f"      = {products}\n"
        f"      = {dot}"
    )
    return prompt, answer


# ---------- 02 matrix multiplication ----------

def matrix_cell_problem(rng: np.random.Generator) -> tuple[str, str]:
    m, k, n = int(rng.integers(2, 4)), int(rng.integers(2, 4)), int(rng.integers(2, 4))
    A = rng.integers(-3, 4, size=(m, k))
    B = rng.integers(-3, 4, size=(k, n))
    i = int(rng.integers(0, m))
    j = int(rng.integers(0, n))
    row, col = A[i], B[:, j]
    val = int(row @ col)
    products = " + ".join(f"({int(x)})({int(y)})" for x, y in zip(row, col))
    prompt = (
        f"Given\n\n"
        f"   A =\n{_fmt_matrix(A)}\n\n"
        f"   B =\n{_fmt_matrix(B)}\n\n"
        f"compute C[{i}, {j}] in C = A · B."
    )
    answer = (
        f"C[{i},{j}] = (row {i} of A) · (col {j} of B)\n"
        f"        = {products}\n"
        f"        = {val}"
    )
    return prompt, answer


# ---------- 03 linear transformations / determinant ----------

def determinant_problem(rng: np.random.Generator) -> tuple[str, str]:
    A = rng.integers(-4, 5, size=(2, 2))
    a, b, c, d = int(A[0, 0]), int(A[0, 1]), int(A[1, 0]), int(A[1, 1])
    det = a * d - b * c
    prompt = (
        f"Compute det(A) for\n\n"
        f"   A =\n{_fmt_matrix(A)}\n\n"
        f"What does its sign and magnitude tell you geometrically?"
    )
    answer = (
        f"det(A) = ad − bc = ({a})({d}) − ({b})({c}) = {a*d} − {b*c} = {det}\n\n"
        f"|det(A)| = {abs(det)}: area scale factor of the transformation.\n"
        f"sign     = {'+' if det > 0 else '−' if det < 0 else '0'}: "
        f"{'orientation preserved' if det > 0 else 'orientation flipped' if det < 0 else 'collapsed (singular)'}."
    )
    return prompt, answer


# ---------- 04 rank ----------

def rank_problem(rng: np.random.Generator) -> tuple[str, str]:
    target_rank = int(rng.integers(1, 4))
    while True:
        if target_rank == 1:
            u = rng.integers(-3, 4, size=(3, 1))
            v = rng.integers(-3, 4, size=(1, 3))
            M = u @ v
        elif target_rank == 2:
            U = rng.integers(-3, 4, size=(3, 2))
            V = rng.integers(-3, 4, size=(2, 3))
            M = U @ V
        else:
            M = rng.integers(-3, 4, size=(3, 3))
        if np.linalg.matrix_rank(M) == target_rank and not np.all(M == 0):
            break
    actual = int(np.linalg.matrix_rank(M))
    prompt = (
        f"What is the rank of\n\n{_fmt_matrix(M)}\n\n"
        f"Recall: rank = number of linearly independent columns (= rows)."
    )
    answer = (
        f"rank(M) = {actual}\n\n"
        f"(numpy.linalg.matrix_rank confirms; equivalently {actual} nonzero singular values.)"
    )
    return prompt, answer


# ---------- 05 eigenvalues ----------

def eigenvalue_problem(rng: np.random.Generator) -> tuple[str, str]:
    while True:
        A = rng.integers(-3, 4, size=(2, 2))
        a, b, c, d = int(A[0, 0]), int(A[0, 1]), int(A[1, 0]), int(A[1, 1])
        tr = a + d
        det = a * d - b * c
        disc = tr * tr - 4 * det
        if disc >= 0:
            break
    sqrt_disc = float(np.sqrt(disc))
    l1 = (tr + sqrt_disc) / 2
    l2 = (tr - sqrt_disc) / 2
    prompt = (
        f"Find the eigenvalues of\n\n{_fmt_matrix(np.array([[a, b], [c, d]]))}\n\n"
        f"Use the characteristic polynomial: det(A − λI) = 0."
    )
    answer = (
        f"tr(A) = {tr}, det(A) = {det}\n"
        f"λ² − tr(A) λ + det(A) = 0  →  λ² − ({tr})λ + ({det}) = 0\n"
        f"discriminant = tr² − 4·det = {tr*tr} − {4*det} = {disc}\n"
        f"λ = (tr ± √Δ) / 2 = ({tr} ± {sqrt_disc:.4f}) / 2\n"
        f"λ₁ ≈ {l1:.4f},   λ₂ ≈ {l2:.4f}"
    )
    return prompt, answer


# ---------- 06 SVD ----------

def svd_singular_values_problem(rng: np.random.Generator) -> tuple[str, str]:
    A = rng.integers(-3, 4, size=(2, 2)).astype(float)
    while np.allclose(A, 0):
        A = rng.integers(-3, 4, size=(2, 2)).astype(float)
    s = np.linalg.svd(A, compute_uv=False)
    AtA = A.T @ A
    eigs = np.sort(np.linalg.eigvalsh(AtA))[::-1]
    prompt = (
        f"Find the singular values of\n\n{_fmt_matrix(A)}\n\n"
        f"Hint: σᵢ = √λᵢ(AᵀA)."
    )
    answer = (
        f"AᵀA =\n{_fmt_matrix(AtA, decimals=2)}\n\n"
        f"eigenvalues of AᵀA: ({eigs[0]:.4f}, {eigs[1]:.4f})\n"
        f"singular values: σ₁ ≈ {s[0]:.4f}, σ₂ ≈ {s[1]:.4f}"
    )
    return prompt, answer


# ---------- 07 projections ----------

def projection_problem(rng: np.random.Generator) -> tuple[str, str]:
    b = rng.integers(-4, 5, size=2)
    u = rng.integers(-4, 5, size=2)
    while np.all(u == 0):
        u = rng.integers(-4, 5, size=2)
    bu = float(b @ u)
    uu = float(u @ u)
    coef = bu / uu
    proj = coef * u
    prompt = (
        f"Project b onto u, where\n\n"
        f"   b = {_fmt_vec(b)}\n"
        f"   u = {_fmt_vec(u)}\n\n"
        f"Formula: proj_u(b) = (b·u / u·u) · u"
    )
    answer = (
        f"b · u = {int(b[0])}·{int(u[0])} + {int(b[1])}·{int(u[1])} = {bu:.0f}\n"
        f"u · u = {int(u[0])}² + {int(u[1])}² = {uu:.0f}\n"
        f"proj = ({bu:.0f}/{uu:.0f}) · u = {coef:.4f} · {_fmt_vec(u)} "
        f"= ({proj[0]:.4f}, {proj[1]:.4f})"
    )
    return prompt, answer


# ---------- 08 PSD ----------

def psd_check_problem(rng: np.random.Generator) -> tuple[str, str]:
    if rng.random() < 0.5:
        L = rng.integers(-3, 4, size=(2, 2)).astype(float)
        L[0, 1] = 0  # lower triangular
        if L[0, 0] == 0:
            L[0, 0] = 1
        M = L @ L.T  # PSD by construction
    else:
        M = rng.integers(-3, 4, size=(2, 2)).astype(float)
        M = (M + M.T) / 2  # symmetric
        # If accidentally PSD, perturb diagonal to be more often indefinite
        if rng.random() < 0.5:
            M[0, 0] -= 4
    eigs = np.sort(np.linalg.eigvalsh(M))
    psd = bool(np.all(eigs >= -1e-9))
    prompt = (
        f"Is the symmetric matrix M PSD (positive semi-definite)?\n\n"
        f"{_fmt_matrix(M, decimals=2)}\n\n"
        f"Recall: M is PSD iff all eigenvalues ≥ 0  iff  vᵀ M v ≥ 0 for all v."
    )
    answer = (
        f"eigenvalues: ({eigs[0]:+.4f}, {eigs[1]:+.4f})\n"
        f"{'All eigenvalues are ≥ 0  →  M is PSD.' if psd else 'At least one eigenvalue is < 0  →  M is NOT PSD.'}"
    )
    return prompt, answer


# ---------- 09 matrix calculus ----------

def gradient_quadratic_problem(rng: np.random.Generator) -> tuple[str, str]:
    while True:
        A = rng.integers(-2, 3, size=(2, 2))
        A = (A + A.T) / 2  # symmetric, integer or half-integer
        if not np.all(A == 0):
            break
    x = rng.integers(-3, 4, size=2)
    grad = 2 * A @ x  # since A symmetric
    prompt = (
        f"Compute ∇ₓ(xᵀ A x) at x = {_fmt_vec(x)} for\n\n"
        f"{_fmt_matrix(A, decimals=1)}\n\n"
        f"Recall: for symmetric A, ∇ₓ(xᵀ A x) = 2 A x."
    )
    answer = (
        f"A x = ({float(A[0,0])}·{int(x[0])} + {float(A[0,1])}·{int(x[1])}, "
        f"{float(A[1,0])}·{int(x[0])} + {float(A[1,1])}·{int(x[1])})\n"
        f"    = ({(A@x)[0]:.2f}, {(A@x)[1]:.2f})\n"
        f"∇ = 2 A x = ({grad[0]:.2f}, {grad[1]:.2f})"
    )
    return prompt, answer


# ---------- 10 cholesky ----------

def cholesky_problem(rng: np.random.Generator) -> tuple[str, str]:
    while True:
        L_true = np.array(
            [
                [rng.integers(1, 4), 0.0],
                [rng.integers(-3, 4), rng.integers(1, 4)],
            ],
            dtype=float,
        )
        M = L_true @ L_true.T
        if np.allclose(M[0, 0], int(M[0, 0])) and np.allclose(M[1, 1], int(M[1, 1])):
            break
    L = np.linalg.cholesky(M)
    prompt = (
        f"Find the Cholesky factor L (lower triangular, L Lᵀ = M) of the PSD matrix\n\n"
        f"{_fmt_matrix(M, decimals=0)}\n\n"
        f"For 2×2 PSD M:  L₁₁ = √M₁₁,   L₂₁ = M₂₁ / L₁₁,   L₂₂ = √(M₂₂ − L₂₁²)."
    )
    answer = (
        f"L₁₁ = √{M[0,0]:.0f} = {L[0,0]:.4f}\n"
        f"L₂₁ = {M[1,0]:.0f} / L₁₁ = {L[1,0]:.4f}\n"
        f"L₂₂ = √({M[1,1]:.0f} − ({L[1,0]:.4f})²) = {L[1,1]:.4f}\n\n"
        f"L =\n{_fmt_matrix(L, decimals=4)}"
    )
    return prompt, answer
