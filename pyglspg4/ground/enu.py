# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# ECEF to ENU (East-North-Up) coordinate transformation
#
# Used for ground-station visibility, azimuth, elevation,
# and Doppler calculations.
#
# References:
#   Vallado, Fundamentals of Astrodynamics and Applications

from __future__ import annotations

import math
from typing import Tuple


def ecef_to_enu(
    r_ecef: Tuple[float, float, float],
    r_site_ecef: Tuple[float, float, float],
    lat_site: float,
    lon_site: float,
) -> Tuple[float, float, float]:
    """
    Convert ECEF satellite position to local ENU coordinates.

    Parameters
    ----------
    r_ecef : (x, y, z)
        Satellite ECEF position (km)
    r_site_ecef : (x, y, z)
        Ground station ECEF position (km)
    lat_site : float
        Ground station geodetic latitude (radians)
    lon_site : float
        Ground station longitude (radians)

    Returns
    -------
    e : float
        East component (km)
    n : float
        North component (km)
    u : float
        Up component (km)
    """

    # Relative position vector
    dx = r_ecef[0] - r_site_ecef[0]
    dy = r_ecef[1] - r_site_ecef[1]
    dz = r_ecef[2] - r_site_ecef[2]

    sin_lat = math.sin(lat_site)
    cos_lat = math.cos(lat_site)
    sin_lon = math.sin(lon_site)
    cos_lon = math.cos(lon_site)

    # Transformation matrix
    e = -sin_lon * dx + cos_lon * dy
    n = -sin_lat * cos_lon * dx - sin_lat * sin_lon * dy + cos_lat * dz
    u =  cos_lat * cos_lon * dx + cos_lat * sin_lon * dy + sin_lat * dz

    return e, n, u

