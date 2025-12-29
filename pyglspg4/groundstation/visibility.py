# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Ground station visibility checks
#
# Determines whether a satellite is visible above a
# given elevation mask.
#
# This module is intentionally simple and composable.
#
# Reference:
#   Vallado, Fundamentals of Astrodynamics and Applications

from __future__ import annotations

import math


def is_visible(
    elevation: float,
    min_elevation: float = 0.0,
) -> bool:
    """
    Determine whether a satellite is visible.

    Parameters
    ----------
    elevation : float
        Elevation angle (rad)
    min_elevation : float, optional
        Minimum elevation mask (rad), default 0 (horizon)

    Returns
    -------
    bool
        True if satellite is above the elevation mask
    """

    return elevation >= min_elevation


def elevation_degrees(elevation: float) -> float:
    """
    Convert elevation angle to degrees.

    Parameters
    ----------
    elevation : float
        Elevation angle (rad)

    Returns
    -------
    float
        Elevation angle (degrees)
    """
    return elevation * 180.0 / math.pi

