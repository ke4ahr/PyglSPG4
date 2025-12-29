# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Time-varying atmospheric drag coupling
#
# Provides optional drag scaling based on space-weather
# parameters (F10.7 solar flux, Ap geomagnetic index).
#
# This module augments — but does NOT replace — the
# NORAD SGP-4 drag model.
#
# Reference:
#   Vallado, Fundamentals of Astrodynamics and Applications
#   Jacchia-Bowman atmospheric models

from __future__ import annotations

from typing import Optional

from pyglspg4.environment.spaceweather import DEFAULT_SPACE_WEATHER


def drag_scale_factor(
    mjd: int,
    base_bstar: float,
) -> float:
    """
    Compute a drag scaling factor based on space weather.

    Parameters
    ----------
    mjd : int
        Modified Julian Date
    base_bstar : float
        Nominal BSTAR drag term from TLE

    Returns
    -------
    float
        Scaled BSTAR value
    """

    sw = DEFAULT_SPACE_WEATHER.get(mjd)
    if sw is None:
        return base_bstar

    # Empirical scaling factors (conservative)
    # Reference solar flux: ~150
    f107_scale = 1.0 + 0.002 * (sw.f107 - 150.0)

    # Geomagnetic storm enhancement
    ap_scale = 1.0 + 0.01 * (sw.ap / 10.0)

    scale = max(0.1, f107_scale * ap_scale)

    return base_bstar * scale


def adjust_bstar(
    mjd: int,
    bstar: float,
    enabled: bool = True,
) -> float:
    """
    Adjust BSTAR drag coefficient using space weather.

    This function is intentionally explicit and opt-in.

    Parameters
    ----------
    mjd : int
        Modified Julian Date
    bstar : float
        Original BSTAR value
    enabled : bool
        Enable time-varying drag

    Returns
    -------
    float
        Adjusted BSTAR value
    """

    if not enabled:
        return bstar

    return drag_scale_factor(mjd, bstar)

