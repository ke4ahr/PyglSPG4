# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Coordinate rotation utilities.

Provides elementary rotations about principal axes, used to transform
orbital-plane coordinates into the Earth-centered inertial (ECI) frame.
"""

from __future__ import annotations

from typing import Sequence

from pyglspg4.backend.base import MathBackend


def rotate_z(v: Sequence[float], angle: float, backend: MathBackend):
    """
    Rotate vector v about the Z-axis by the given angle (radians).
    """
    c = backend.cos(angle)
    s = backend.sin(angle)
    return (
        c * v[0] - s * v[1],
        s * v[0] + c * v[1],
        v[2],
    )


def rotate_x(v: Sequence[float], angle: float, backend: MathBackend):
    """
    Rotate vector v about the X-axis by the given angle (radians).
    """
    c = backend.cos(angle)
    s = backend.sin(angle)
    return (
        v[0],
        c * v[1] - s * v[2],
        s * v[1] + c * v[2],
    )

