# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Doppler shift computation
#
# Computes Doppler frequency correction for satellite
# communication links based on relative line-of-sight
# velocity.
#
# Reference:
#   Vallado, Fundamentals of Astrodynamics and Applications

from __future__ import annotations

import math
from typing import Tuple

# Speed of light (km/s)
C_KM_S = 299792.458


def doppler_shift(
    r_sat: Tuple[float, float, float],
    v_sat: Tuple[float, float, float],
    r_site: Tuple[float, float, float],
    v_site: Tuple[float, float, float],
    f0: float,
) -> float:
    """
    Compute Doppler-shifted frequency.

    Parameters
    ----------
    r_sat : tuple
        Satellite position in ITRF (km)
    v_sat : tuple
        Satellite velocity in ITRF (km/s)
    r_site : tuple
        Ground station position in ITRF (km)
    v_site : tuple
        Ground station velocity in ITRF (km/s)
    f0 : float
        Nominal transmit frequency (Hz)

    Returns
    -------
    float
        Doppler-shifted frequency (Hz)
    """

    # Line-of-sight vector
    rx = r_sat[0] - r_site[0]
    ry = r_sat[1] - r_site[1]
    rz = r_sat[2] - r_site[2]

    rho = math.sqrt(rx * rx + ry * ry + rz * rz)
    if rho <= 0.0:
        return f0

    # Relative velocity
    dvx = v_sat[0] - v_site[0]
    dvy = v_sat[1] - v_site[1]
    dvz = v_sat[2] - v_site[2]

    # Range rate (projection onto LOS)
    range_rate = (rx * dvx + ry * dvy + rz * dvz) / rho

    # Doppler formula
    return f0 * (1.0 - range_rate / C_KM_S)

