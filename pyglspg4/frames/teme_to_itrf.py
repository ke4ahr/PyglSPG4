# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# TEME -> ITRF (ECEF) frame transformation
#
# Applies Earth rotation, UT1 correction, and
# polar motion using IERS Earth Orientation Parameters.
#
# References:
#   Vallado, Fundamentals of Astrodynamics and Applications
#   IERS Conventions (2010)

from __future__ import annotations

import math
from typing import Tuple

from pyglspg4.frames.eop import EOPTable
from pyglspg4.frames.sidereal import earth_rotation_angle
from pyglspg4.frames.polar_motion import (
    polar_motion_matrix,
    apply_polar_motion,
)
from pyglspg4.time.julian import jd_to_mjd


def teme_to_itrf(
    r_teme: Tuple[float, float, float],
    v_teme: Tuple[float, float, float],
    jd_utc: float,
    eop: EOPTable,
) -> Tuple[
    Tuple[float, float, float],
    Tuple[float, float, float],
]:
    """
    Convert TEME position/velocity to ITRF (ECEF).

    Parameters
    ----------
    r_teme : (x, y, z)
        TEME position vector (km)
    v_teme : (vx, vy, vz)
        TEME velocity vector (km/s)
    jd_utc : float
        Julian Date UTC
    eop : EOPTable
        Loaded Earth Orientation Parameters

    Returns
    -------
    r_itrf : (x, y, z)
        ITRF/ECEF position (km)
    v_itrf : (vx, vy, vz)
        ITRF/ECEF velocity (km/s)
    """

    # ------------------------------------------------------------------
    # 1. Convert UTC to UT1 using EOP
    # ------------------------------------------------------------------
    mjd_utc = jd_to_mjd(jd_utc)
    eop_rec = eop.interpolate(mjd_utc)

    jd_ut1 = jd_utc + eop_rec.ut1_utc / 86400.0

    # ------------------------------------------------------------------
    # 2. Earth rotation angle
    # ------------------------------------------------------------------
    theta = earth_rotation_angle(jd_ut1)
    c = math.cos(theta)
    s = math.sin(theta)

    # Rotation matrix about Z
    rot = (
        ( c,  s, 0.0),
        (-s,  c, 0.0),
        (0.0, 0.0, 1.0),
    )

    # Rotate position
    r_pef = (
        rot[0][0] * r_teme[0] + rot[0][1] * r_teme[1],
        rot[1][0] * r_teme[0] + rot[1][1] * r_teme[1],
        r_teme[2],
    )

    # Rotate velocity (Earth rotation term)
    omega_earth = 7.2921150e-5  # rad/s

    v_pef = (
        rot[0][0] * v_teme[0] + rot[0][1] * v_teme[1] + omega_earth * r_pef[1],
        rot[1][0] * v_teme[0] + rot[1][1] * v_teme[1] - omega_earth * r_pef[0],
        v_teme[2],
    )

    # ------------------------------------------------------------------
    # 3. Apply polar motion
    # ------------------------------------------------------------------
    pm = polar_motion_matrix(
        eop_rec.xp_arcsec,
        eop_rec.yp_arcsec,
    )

    r_itrf = apply_polar_motion(r_pef, pm)
    v_itrf = apply_polar_motion(v_pef, pm)

    return r_itrf, v_itrf

