# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# ECEF <-> geodetic coordinate transformations
#
# Implements WGS-84 Earth model.
#
# References:
#   Vallado, Fundamentals of Astrodynamics and Applications
#   NGA TR8350.2

from __future__ import annotations

import math
from typing import Tuple


# WGS-84 constants
WGS84_A = 6378.137            # km
WGS84_F = 1.0 / 298.257223563
WGS84_E2 = WGS84_F * (2.0 - WGS84_F)


def ecef_to_geodetic(
    x: float,
    y: float,
    z: float,
) -> Tuple[float, float, float]:
    """
    Convert ECEF coordinates to geodetic latitude, longitude, altitude.

    Parameters
    ----------
    x, y, z : float
        ECEF coordinates (km)

    Returns
    -------
    lat : float
        Geodetic latitude (radians)
    lon : float
        Longitude (radians)
    alt : float
        Altitude above ellipsoid (km)
    """

    lon = math.atan2(y, x)
    r = math.hypot(x, y)

    lat = math.atan2(z, r * (1.0 - WGS84_E2))
    for _ in range(5):
        sin_lat = math.sin(lat)
        N = WGS84_A / math.sqrt(1.0 - WGS84_E2 * sin_lat * sin_lat)
        alt = r / math.cos(lat) - N
        lat = math.atan2(z, r * (1.0 - WGS84_E2 * N / (N + alt)))

    return lat, lon, alt

