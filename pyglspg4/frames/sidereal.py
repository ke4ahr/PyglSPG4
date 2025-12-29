# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Sidereal time and Earth rotation utilities
#
# Implements Greenwich Mean Sidereal Time (GMST)
# suitable for TEME -> Earth-fixed transformations.
#
# References:
#   Vallado, Fundamentals of Astrodynamics and Applications
#   IAU 2006 precession model (simplified GMST)

from __future__ import annotations

import math

from pyglspg4.time.julian import jd_to_mjd


SECONDS_PER_DAY = 86400.0
TWO_PI = 2.0 * math.pi


def gmst_from_ut1(jd_ut1: float) -> float:
    """
    Compute Greenwich Mean Sidereal Time (GMST).

    Parameters
    ----------
    jd_ut1 : float
        Julian Date in UT1 time scale

    Returns
    -------
    gmst : float
        Greenwich Mean Sidereal Time (radians),
        normalized to [0, 2π)
    """

    # Convert JD to centuries since J2000
    T = (jd_ut1 - 2451545.0) / 36525.0

    # Vallado Eq. 3-41 (arcseconds)
    gmst_sec = (
        67310.54841
        + (876600.0 * 3600.0 + 8640184.812866) * T
        + 0.093104 * T * T
        - 6.2e-6 * T * T * T
    )

    # Convert to radians
    gmst_rad = (gmst_sec % SECONDS_PER_DAY) * (TWO_PI / SECONDS_PER_DAY)

    return gmst_rad


def earth_rotation_angle(jd_ut1: float) -> float:
    """
    Compute Earth Rotation Angle (ERA).

    This is equivalent to GMST for SGP-4 accuracy
    and used internally for TEME -> ITRF.

    Parameters
    ----------
    jd_ut1 : float
        Julian Date UT1

    Returns
    -------
    era : float
        Earth rotation angle (radians)
    """

    d = jd_ut1 - 2451545.0
    f = d % 1.0

    era = TWO_PI * (f + 0.7790572732640 + 0.00273781191135448 * d)
    return era % TWO_PI

