# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# TEME → PEF frame transformation.
# Uses GMST rotation only (no polar motion).

import math
from pyglspg4.frames.gmst import gmst_from_ut1


def teme_to_pef(pos_teme_km, jd_ut1):
    """
    Transform TEME position to Pseudo-Earth-Fixed (PEF).

    Parameters
    ----------
    pos_teme_km : tuple(float, float, float)
        TEME position vector in km
    jd_ut1 : float
        Julian date UT1

    Returns
    -------
    tuple(float, float, float)
        PEF position vector in km
    """

    theta = gmst_from_ut1(jd_ut1)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    x, y, z = pos_teme_km

    xp =  cos_t * x + sin_t * y
    yp = -sin_t * x + cos_t * y
    zp =  z

    return (xp, yp, zp)

