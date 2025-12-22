# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Reference validation helpers.

Intended for comparison against Vallado SGP-4 test vectors.
"""

from __future__ import annotations

from math import sqrt


def position_error_km(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    return sqrt(dx * dx + dy * dy + dz * dz)


def velocity_error_km_s(v1, v2):
    dx = v1[0] - v2[0]
    dy = v1[1] - v2[1]
    dz = v1[2] - v2[2]
    return sqrt(dx * dx + dy * dy + dz * dz)

