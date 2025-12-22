# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Vector math utilities.

Lightweight helpers for 3D vector operations used throughout
SGP-4 and SDP-4 propagation. Implemented without external
dependencies to remain backend-agnostic.
"""

from __future__ import annotations

from typing import Sequence


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    """
    Compute the dot product of two 3D vectors.
    """
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm(v: Sequence[float]) -> float:
    """
    Compute the Euclidean norm of a 3D vector.
    """
    return (v[0] * v[0] + v[1] * v[1] + v[2] * v[2]) ** 0.5

