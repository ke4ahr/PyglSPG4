# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# PEF → ITRF frame transformation.
# Applies polar motion using IERS EOP parameters xp, yp (radians).

import math


def pef_to_itrf(pos_pef_km, xp_rad=0.0, yp_rad=0.0):
    """
    Transform PEF position to ITRF (ECEF).

    Parameters
    ----------
    pos_pef_km : tuple(float, float, float)
        PEF position vector in km
    xp_rad : float
        Polar motion x (radians)
    yp_rad : float
        Polar motion y (radians)

    Returns
    -------
    tuple(float, float, float)
        ITRF position vector in km
    """

    x, y, z = pos_pef_km

    # Small-angle polar motion rotation
    x_itrf = x + xp_rad * z
    y_itrf = y - yp_rad * z
    z_itrf = z - xp_rad * x + yp_rad * y

    return (x_itrf, y_itrf, z_itrf)

