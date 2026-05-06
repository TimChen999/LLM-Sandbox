"""Pytest configuration: make the visual-explainers root importable.

Lets tests do `from modules.linear_algebra import ...` regardless of where
pytest is invoked from.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
