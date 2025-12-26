# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# ITRF (ECEF) → Geodetic latitude, longitude, altitude.
# Uses WGS-84 ellipsoid.

import math

WGS84_A = 6378.137
WGS84_F = 1.0 / 298.257223563
WGS84_E2 = WGS84_F * (2.0 - WGS84_F)


def itrf_to_geodetic(pos_itrf_km):
    """
    Convert ECEF (ITRF) position to geodetic coordinates.

    Parameters
    ----------
    pos_itrf_km : tuple(float, float, float)
        Position in km

    Returns
    -------
    (lat_rad, lon_rad, alt_km)
    """

    x, y, z = pos_itrf_km

    lon = math.atan2(y, x)
    r = math.hypot(x, y)

    lat = math.atan2(z, r)
    for _ in range(5):
        sin_lat = math.sin(lat)
        N = WGS84_A / math.sqrt(1.0 - WGS84_E2 * sin_lat * sin_lat)
        lat = math.atan2(z + WGS84_E2 * N * sin_lat, r)

    alt = r / math.cos(lat) - N

    return lat, lon, alt

