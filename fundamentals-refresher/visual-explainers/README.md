# Visual Explainers

A native Tkinter desktop app for the math in [`../README.md`](../README.md). No browser, no server, no Streamlit.

Animated, interactive demos of the math used in machine learning. Each view calls a **tested** pure-math function from `modules/`, so the picture cannot show wrong values.

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

That `.exe` is **fully standalone** — copy it anywhere, double-click it, the app runs. No Python install, no venv, no terminal window.

To rebuild after code changes, just run `build.bat` again.

## Run the tests

```powershell
.venv\Scripts\pytest
```

## Structure

```
visual-explainers/
  app.py                    # Tk root window + top-level navigation
  views/                    # Tk frames; one file per demo
    linear_algebra_tab.py   # Groups the linear-algebra sub-tabs
    matrix_mult_view.py     # Animated step-by-step matrix multiplication
    power_iteration_view.py # Animated power-iteration eigenvector convergence
  modules/                  # Pure math functions, no GUI
    linear_algebra.py
  tests/                    # pytest tests for the math modules
    test_linear_algebra.py
  conftest.py
  requirements.txt
  build.bat                 # PyInstaller -> dist\visual-explainers.exe
  launch_dev.bat            # python app.py via venv
```

## Adding a new topic

1. Add pure functions to a new file in `modules/`. No tkinter, no matplotlib.
2. Add tests in `tests/` — at least one known-answer test, one cross-check vs. numpy/scipy, and one property invariant.
3. Add a Tk frame in `views/` that imports those functions and animates them.
4. Wire the new frame into `app.py` (top-level tab) or into an existing topic-area tab.

The math/visualization split is the whole point — keep tests on the math, trust the visualization by construction.
