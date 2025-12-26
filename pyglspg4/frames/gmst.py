# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Greenwich Mean Sidereal Time (GMST) computation.
# Vallado Eq. 3-41, IAU-82 compatible.

import math

TWOPI = 2.0 * math.pi
SECONDS_PER_DAY = 86400.0


def gmst_from_ut1(jd_ut1):
    """
    Compute Greenwich Mean Sidereal Time (radians).

    Parameters
    ----------
    jd_ut1 : float
        Julian Date in UT1 time scale

    Returns
    -------
    float
        GMST angle in radians, normalized to [0, 2π)
    """

    T = (jd_ut1 - 2451545.0) / 36525.0

    gmst_sec = (
        67310.54841
        + (876600.0 * 3600.0 + 8640184.812866) * T
        + 0.093104 * T * T
        - 6.2e-6 * T * T * T
    )

    return (gmst_sec % SECONDS_PER_DAY) * (TWOPI / SECONDS_PER_DAY)

