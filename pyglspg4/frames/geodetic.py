# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# ECEF -> Geodetic conversion
#
# Converts Earth-Centered Earth-Fixed (ECEF) coordinates
# to geodetic latitude, longitude, and altitude using
# the WGS-84 reference ellipsoid.
#
# Reference:
#   Vallado, Fundamentals of Astrodynamics and Applications
#   NGA TR8350.2

from __future__ import annotations

import math
from typing import Tuple

# WGS-84 constants
WGS84_A = 6378.137            # semi-major axis (km)
WGS84_F = 1.0 / 298.257223563
WGS84_B = WGS84_A * (1.0 - WGS84_F)
WGS84_E2 = WGS84_F * (2.0 - WGS84_F)


def ecef_to_geodetic(
    r_ecef: Tuple[float, float, float],
) -> Tuple[float, float, float]:
    """
    Convert ECEF coordinates to geodetic latitude,
    longitude, and altitude.

    Parameters
    ----------
    r_ecef : tuple
        Position vector in ECEF frame (km)

    Returns
    -------
    (lat, lon, alt)
        Latitude (rad), longitude (rad), altitude (km)
    """

    x, y, z = r_ecef

    lon = math.atan2(y, x)

    r_xy = math.hypot(x, y)
    if r_xy < 1e-12:
        # At the poles
        lat = math.copysign(math.pi / 2.0, z)
        alt = abs(z) - WGS84_B
        return lat, lon, alt

    # Bowring's method
    theta = math.atan2(z * WGS84_A, r_xy * WGS84_B)
    sin_t = math.sin(theta)
    cos_t = math.cos(theta)

    lat = math.atan2(
        z + (WGS84_E2 * WGS84_B) * sin_t ** 3,
        r_xy - (WGS84_E2 * WGS84_A) * cos_t ** 3,
    )

    sin_lat = math.sin(lat)
    n = WGS84_A / math.sqrt(1.0 - WGS84_E2 * sin_lat * sin_lat)

    alt = r_xy / math.cos(lat) - n

    return lat, lon, alt

