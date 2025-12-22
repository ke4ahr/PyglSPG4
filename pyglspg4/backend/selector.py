# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Runtime backend selection.

Selects an appropriate numerical backend (pure Python or NumPy)
based on user preference and availability.
"""

from __future__ import annotations

from pyglspg4.backend.python import PythonBackend


def select_backend(prefer: str | None = None):
    """
    Select and instantiate a math backend.

    Args:
        prefer: Optional backend preference. Supported values:
                - "numpy": prefer NumPy backend if available
                - None or any other value: use pure-Python backend

    Returns:
        An instance implementing the MathBackend protocol.
    """
    if prefer == "numpy":
        try:
            from pyglspg4.backend.numpy import NumPyBackend
            return NumPyBackend()
        except Exception:
            pass

    return PythonBackend()

