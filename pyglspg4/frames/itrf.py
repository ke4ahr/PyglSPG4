# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# TEME -> ITRF frame transformation
#
# Implements the full transformation chain:
#   TEME -> ECEF (PEF) -> ITRF
#
# Including:
#   - Earth rotation via GMST
#   - Polar motion (xp, yp) via IERS EOP
#
# Reference:
#   Vallado, Fundamentals of Astrodynamics and Applications
#   IERS Conventions (2010)

from __future__ import annotations

import math
from typing import Tuple

from pyglspg4.frames.gmst import gmst_from_jd
from pyglspg4.frames.eop import DEFAULT_EOP
from pyglspg4.frames.teme_to_ecef import OMEGA_EARTH

ARCSEC_TO_RAD = math.pi / (180.0 * 3600.0)


def _polar_motion_matrix(xp_rad: float, yp_rad: float):
    """
    Construct polar motion rotation matrix.
    """
    cx = math.cos(xp_rad)
    sx = math.sin(xp_rad)
    cy = math.cos(yp_rad)
    sy = math.sin(yp_rad)

    return (
        (cy, 0.0, sy),
        (sx * sy, cx, -sx * cy),
        (-cx * sy, sx, cx * cy),
    )


def _mat_vec(m, v):
    return (
        m[0][0] * v[0] + m[0][1] * v[1] + m[0][2] * v[2],
        m[1][0] * v[0] + m[1][1] * v[1] + m[1][2] * v[2],
        m[2][0] * v[0] + m[2][1] * v[1] + m[2][2] * v[2],
    )


def teme_to_itrf(
    r_teme: Tuple[float, float, float],
    v_teme: Tuple[float, float, float],
    jd_ut1: float,
) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    """
    Convert TEME position and velocity vectors to ITRF.

    Parameters
    ----------
    r_teme : tuple
        TEME position vector (km)
    v_teme : tuple
        TEME velocity vector (km/s)
    jd_ut1 : float
        Julian Date (UT1)

    Returns
    -------
    (r_itrf, v_itrf)
        Position and velocity in ITRF frame
    """

    # Step 1: TEME -> ECEF via Earth rotation
    theta = gmst_from_jd(jd_ut1)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    r_ecef = (
        cos_t * r_teme[0] + sin_t * r_teme[1],
        -sin_t * r_teme[0] + cos_t * r_teme[1],
        r_teme[2],
    )

    v_rot = (
        cos_t * v_teme[0] + sin_t * v_teme[1],
        -sin_t * v_teme[0] + cos_t * v_teme[1],
        v_teme[2],
    )

    omega_cross_r = (
        -OMEGA_EARTH * r_ecef[1],
        OMEGA_EARTH * r_ecef[0],
        0.0,
    )

    v_ecef = (
        v_rot[0] + omega_cross_r[0],
        v_rot[1] + omega_cross_r[1],
        v_rot[2] + omega_cross_r[2],
    )

    # Step 2: Polar motion (ECEF -> ITRF)
    mjd = int(jd_ut1 - 2400000.5)
    eop = DEFAULT_EOP.get(mjd)

    if eop is not None:
        xp = eop.xp * ARCSEC_TO_RAD
        yp = eop.yp * ARCSEC_TO_RAD
    else:
        xp = 0.0
        yp = 0.0

    pm = _polar_motion_matrix(xp, yp)

    r_itrf = _mat_vec(pm, r_ecef)
    v_itrf = _mat_vec(pm, v_ecef)

    return r_itrf, v_itrf

