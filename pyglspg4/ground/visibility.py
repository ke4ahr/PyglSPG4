# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Ground-station visibility and Doppler computation
#
# Computes azimuth, elevation, range, range-rate,
# and Doppler shift for satellite tracking.
#
# References:
#   Vallado, Fundamentals of Astrodynamics and Applications

from __future__ import annotations

import math
from typing import Tuple

from pyglspg4.ground.refraction import refraction_correction


C_LIGHT = 299792.458  # km/s


def az_el_range(
    e: float,
    n: float,
    u: float,
) -> Tuple[float, float, float]:
    """
    Compute azimuth, elevation, and range from ENU coordinates.

    Parameters
    ----------
    e, n, u : float
        ENU coordinates (km)

    Returns
    -------
    az : float
        Azimuth (radians, measured east from north)
    el : float
        Elevation (radians)
    rng : float
        Slant range (km)
    """

    rng = math.sqrt(e * e + n * n + u * u)

    az = math.atan2(e, n)
    if az < 0.0:
        az += 2.0 * math.pi

    el = math.asin(u / rng)

    return az, el, rng


def apply_refraction(
    elevation_rad: float,
    pressure_hpa: float = 1010.0,
    temperature_c: float = 10.0,
) -> float:
    """
    Apply atmospheric refraction correction to elevation.

    Returns corrected elevation angle.
    """

    return elevation_rad + refraction_correction(
        elevation_rad,
        pressure_hpa,
        temperature_c,
    )


def range_rate(
    e: float,
    n: float,
    u: float,
    ve: float,
    vn: float,
    vu: float,
) -> float:
    """
    Compute slant range rate.

    Parameters
    ----------
    e, n, u : float
        ENU position (km)
    ve, vn, vu : float
        ENU velocity (km/s)

    Returns
    -------
    rr : float
        Range rate (km/s)
    """

    rng = math.sqrt(e * e + n * n + u * u)
    return (e * ve + n * vn + u * vu) / rng


def doppler_shift(
    range_rate_km_s: float,
    frequency_hz: float,
) -> float:
    """
    Compute Doppler frequency shift.

    Parameters
    ----------
    range_rate_km_s : float
        Range rate (km/s), positive if receding
    frequency_hz : float
        Transmit frequency (Hz)

    Returns
    -------
    delta_f : float
        Doppler shift (Hz)
    """

    return -frequency_hz * (range_rate_km_s / C_LIGHT)

