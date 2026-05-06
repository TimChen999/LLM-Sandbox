# Visual Explainers — Linear Algebra Curriculum

A native Tkinter desktop app: 10 ordered linear-algebra topics, each with a short overview, an interactive visual demo with step-by-step calculations, and randomly generated practice problems. No browser, no server.

## Curriculum

1. Vectors, dot products, norms
2. Matrix multiplication
3. Linear transformations
4. Rank, null space, column space
5. Eigenvalues and eigenvectors
6. Singular Value Decomposition (SVD)
7. Projections and least squares
8. Positive (semi)definite matrices
9. Matrix calculus (gradients, Jacobians, Hessians)
10. Matrix factorizations (QR, LU, Cholesky)

Each topic page has two tabs: **Demo** (visual + calculations) and **Practice** (random problems with reveal-answer).

## Run it (the one button)

**Double-click `Launch.bat`.** That's it.

On first run it sets up the virtual environment, installs dependencies, builds the standalone `.exe`, and launches the app — about 1–3 minutes one-time. On every subsequent launch it starts instantly. If you edit the source code, the launcher detects the change and rebuilds automatically before launching.

Requires Python 3.10+ on your PATH for the first-time setup.

## Other ways to run (optional)

- `dist\visual-explainers.exe` — once built by `Launch.bat`, this is fully standalone. Copy it anywhere; no Python needed. Make a desktop shortcut if you like.
- `launch_dev.bat` — runs from source via the venv (skips the build step). Faster iteration when changing code.
- `build.bat` — verbose rebuild for debugging build failures.

## Run the tests

```powershell
.venv\Scripts\pytest
```

## Structure

```
visual-explainers/
  app.py                          # Tk root: sidebar nav + content swap
  curriculum/
    __init__.py                   # exports TOPICS list (in order)
    base.py                       # TopicFrame: shared header + Demo/Practice tabs
    home.py                       # front-page cards
    practice_widget.py            # New problem / Show answer panel
    t01_vectors.py … t10_factorizations.py   # one file per topic
  views/                          # Tk frames; one per visual demo
    vectors_view.py
    matrix_mult_view.py
    transformations_view.py
    rank_view.py
    power_iteration_view.py
    svd_view.py
    projections_view.py
    psd_view.py
    matrix_calculus_view.py
    factorizations_view.py
  modules/                        # pure math, no GUI imports
    linear_algebra.py             # operations used by views (tested vs numpy)
    practice.py                   # random problem generators
  tests/
    test_linear_algebra.py
    test_practice.py
  conftest.py
  requirements.txt
  build.bat                       # PyInstaller -> dist\visual-explainers.exe
  launch_dev.bat                  # python app.py via venv
```

## Adding a new topic

1. **Math**: add pure functions to `modules/` if needed; add tests in `tests/`.
2. **Practice**: add a generator `xxx_problem(rng) -> (prompt, answer)` to `modules/practice.py`; add a test in `tests/test_practice.py`.
3. **Visual**: add a Tk Frame subclass in `views/yourtopic_view.py` with sliders + a matplotlib `Figure` + a calculation panel (always pack the calc panel first with `side="bottom"`, then the canvas with `expand=True`, or the canvas will hide it).
4. **Topic**: add `curriculum/tNN_yourtopic.py` extending `TopicFrame` with `TITLE / BUILDS_ON / OVERVIEW` and the `build_demo` / `build_practice` hooks.
5. **Register**: import the topic class in `curriculum/__init__.py` and add it to `TOPICS`.

The math layer is tested; visual layer trusts the math by construction.
