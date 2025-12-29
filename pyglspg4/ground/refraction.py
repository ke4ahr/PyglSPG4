# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Atmospheric refraction correction
#
# Implements the Bennett (1982) refraction model,
# suitable for satellite tracking and pass prediction.
#
# References:
#   Bennett, G.G., "The Calculation of Astronomical Refraction"
#   Vallado, Fundamentals of Astrodynamics and Applications

from __future__ import annotations

import math


def refraction_correction(
    elevation_rad: float,
    pressure_hpa: float = 1010.0,
    temperature_c: float = 10.0,
) -> float:
    """
    Compute atmospheric refraction correction.

    Parameters
    ----------
    elevation_rad : float
        Geometric elevation angle (radians)
    pressure_hpa : float
        Surface pressure (hPa)
    temperature_c : float
        Surface temperature (Celsius)

    Returns
    -------
    delta_elevation : float
        Refraction correction to add to elevation (radians)
    """

    # Below horizon, refraction is undefined
    if elevation_rad < -0.01:
        return 0.0

    # Convert to degrees
    elev_deg = math.degrees(elevation_rad)

    # Bennett (1982) formula (arcminutes)
    R_arcmin = (
        1.02 /
        math.tan(math.radians(elev_deg + 10.3 / (elev_deg + 5.11)))
    )

    # Scale for pressure and temperature
    R_arcmin *= (pressure_hpa / 1010.0) * (283.0 / (273.0 + temperature_c))

    # Convert arcminutes to radians
    return math.radians(R_arcmin / 60.0)

