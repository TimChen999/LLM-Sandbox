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

## Setup (one time)

From this directory, in PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

## Run during development

Double-click `launch_dev.bat`, or:
```powershell
.venv\Scripts\python app.py
```

## Build a standalone .exe

Double-click `build.bat`. After ~1–3 minutes you'll get:

```
dist\visual-explainers.exe
```

That `.exe` is fully standalone — copy it anywhere, double-click it, the app runs. No Python install, no venv, no terminal window. Rebuild after code changes by running `build.bat` again.

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
