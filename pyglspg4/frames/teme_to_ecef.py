# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# TEME -> ECEF frame transformation
#
# Implements the standard SGP-4 compatible transformation
# from True Equator Mean Equinox (TEME) to Earth-Centered
# Earth-Fixed (ECEF).
#
# Reference:
#   Vallado, Fundamentals of Astrodynamics and Applications
#   AIAA 2006-6753
#
# Notes:
#   - No equation of equinoxes is applied (TEME convention)
#   - Suitable for ground station and pass prediction use

from __future__ import annotations

import math

from pyglspg4.frames.gmst import gmst_from_jd

# Earth rotation rate (rad/s)
OMEGA_EARTH = 7.2921150e-5


def teme_to_ecef(
    r_teme: tuple[float, float, float],
    v_teme: tuple[float, float, float],
    jd_ut1: float,
) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    """
    Convert TEME position and velocity vectors to ECEF.

    Parameters
    ----------
    r_teme : (float, float, float)
        Position vector in TEME frame (km)
    v_teme : (float, float, float)
        Velocity vector in TEME frame (km/s)
    jd_ut1 : float
        Julian Date (UT1)

    Returns
    -------
    (r_ecef, v_ecef)
        Position and velocity in ECEF frame
    """

    theta = gmst_from_jd(jd_ut1)

    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    # Rotation matrix about Z-axis
    r_ecef = (
        cos_t * r_teme[0] + sin_t * r_teme[1],
        -sin_t * r_teme[0] + cos_t * r_teme[1],
        r_teme[2],
    )

    # Velocity rotation
    v_rot = (
        cos_t * v_teme[0] + sin_t * v_teme[1],
        -sin_t * v_teme[0] + cos_t * v_teme[1],
        v_teme[2],
    )

    # Earth rotation cross product (ω × r)
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

    return r_ecef, v_ecef

