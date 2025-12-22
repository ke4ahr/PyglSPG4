# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Runtime backend selection.
"""

from __future__ import annotations

from pyglspg4.backend.python import PythonBackend


def select_backend(prefer: str | None = None):
    if prefer == "numpy":
        try:
            from pyglspg4.backend.numpy import NumPyBackend
            return NumPyBackend()
        except Exception:
            return PythonBackend()
    return PythonBackend()

