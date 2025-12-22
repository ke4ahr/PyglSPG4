# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Coordinate rotation utilities.
"""

from __future__ import annotations

from typing import Sequence

from pyglspg4.backend.base import MathBackend


def rotate_z(v: Sequence[float], angle: float, backend: MathBackend):
    c = backend.cos(angle)
    s = backend.sin(angle)
    return (
        c * v[0] - s * v[1],
        s * v[0] + c * v[1],
        v[2],
    )


def rotate_x(v: Sequence[float], angle: float, backend: MathBackend):
    c = backend.cos(angle)
    s = backend.sin(angle)
    return (
        v[0],
        c * v[1] - s * v[2],
        s * v[1] + c * v[2],
    )

