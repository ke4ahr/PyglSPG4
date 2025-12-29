# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Topocentric coordinate conversion
#
# Converts satellite ITRF position vectors into
# azimuth, elevation, and range relative to a
# ground station.
#
# Reference:
#   Vallado, Fundamentals of Astrodynamics and Applications

from __future__ import annotations

import math
from typing import Tuple

from pyglspg4.frames.geodetic import WGS84_A, WGS84_E2


def _geodetic_to_ecef(
    lat: float,
    lon: float,
    alt: float,
) -> Tuple[float, float, float]:
    """
    Convert geodetic coordinates to ECEF.

    Parameters
    ----------
    lat : float
        Latitude (rad)
    lon : float
        Longitude (rad)
    alt : float
        Altitude above ellipsoid (km)
    """

    sin_lat = math.sin(lat)
    cos_lat = math.cos(lat)
    sin_lon = math.sin(lon)
    cos_lon = math.cos(lon)

    n = WGS84_A / math.sqrt(1.0 - WGS84_E2 * sin_lat * sin_lat)

    x = (n + alt) * cos_lat * cos_lon
    y = (n + alt) * cos_lat * sin_lon
    z = (n * (1.0 - WGS84_E2) + alt) * sin_lat

    return x, y, z


def topocentric(
    r_itrf: Tuple[float, float, float],
    lat: float,
    lon: float,
    alt: float,
) -> Tuple[float, float, float]:
    """
    Compute topocentric azimuth, elevation, and range.

    Parameters
    ----------
    r_itrf : tuple
        Satellite position in ITRF (km)
    lat : float
        Ground station latitude (rad)
    lon : float
        Ground station longitude (rad)
    alt : float
        Ground station altitude (km)

    Returns
    -------
    (az, el, rho)
        Azimuth (rad), elevation (rad), range (km)
    """

    # Ground station position in ECEF
    r_site = _geodetic_to_ecef(lat, lon, alt)

    # Vector from site to satellite
    dx = r_itrf[0] - r_site[0]
    dy = r_itrf[1] - r_site[1]
    dz = r_itrf[2] - r_site[2]

    sin_lat = math.sin(lat)
    cos_lat = math.cos(lat)
    sin_lon = math.sin(lon)
    cos_lon = math.cos(lon)

    # ENU coordinates
    east = -sin_lon * dx + cos_lon * dy
    north = -sin_lat * cos_lon * dx - sin_lat * sin_lon * dy + cos_lat * dz
    up = cos_lat * cos_lon * dx + cos_lat * sin_lon * dy + sin_lat * dz

    rho = math.sqrt(east * east + north * north + up * up)
    az = math.atan2(east, north)
    if az < 0.0:
        az += 2.0 * math.pi

    el = math.asin(up / rho)

    return az, el, rho

