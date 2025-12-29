# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Polar motion transformation
#
# Applies IERS polar motion corrections (xp, yp)
# to rotate from Earth rotation frame into ITRF.
#
# References:
#   IERS Conventions (2010)
#   Vallado, Fundamentals of Astrodynamics and Applications

from __future__ import annotations

import math
from typing import Tuple


ARCSEC_TO_RAD = math.pi / (180.0 * 3600.0)


def polar_motion_matrix(
    xp_arcsec: float,
    yp_arcsec: float,
) -> Tuple[
    Tuple[float, float, float],
    Tuple[float, float, float],
    Tuple[float, float, float],
]:
    """
    Construct polar motion rotation matrix.

    Parameters
    ----------
    xp_arcsec : float
        Polar motion x (arcseconds)
    yp_arcsec : float
        Polar motion y (arcseconds)

    Returns
    -------
    pm : 3x3 rotation matrix
        Polar motion matrix
    """

    xp = xp_arcsec * ARCSEC_TO_RAD
    yp = yp_arcsec * ARCSEC_TO_RAD

    cx = math.cos(xp)
    sx = math.sin(xp)
    cy = math.cos(yp)
    sy = math.sin(yp)

    # Rotation: Ry(-xp) * Rx(-yp)
    return (
        ( cy,        0.0, -sy),
        ( sx * sy,   cx,  sx * cy),
        ( cx * sy,  -sx,  cx * cy),
    )


def apply_polar_motion(
    r: Tuple[float, float, float],
    pm: Tuple[
        Tuple[float, float, float],
        Tuple[float, float, float],
        Tuple[float, float, float],
    ],
) -> Tuple[float, float, float]:
    """
    Apply polar motion matrix to a vector.

    Parameters
    ----------
    r : (x, y, z)
        Vector in Earth rotation frame
    pm : 3x3 matrix
        Polar motion matrix

    Returns
    -------
    r_itrf : (x, y, z)
        Vector in ITRF/ECEF frame
    """

    return (
        pm[0][0] * r[0] + pm[0][1] * r[1] + pm[0][2] * r[2],
        pm[1][0] * r[0] + pm[1][1] * r[1] + pm[1][2] * r[2],
        pm[2][0] * r[0] + pm[2][1] * r[1] + pm[2][2] * r[2],
    )

