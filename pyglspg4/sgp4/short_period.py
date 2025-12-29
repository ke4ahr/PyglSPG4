# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SGP-4 short-period gravitational corrections
# Implements Vallado (2006) Section 4.3 exactly
#
# This module applies J2/J4 short-period periodic corrections
# after secular + drag updates and before position/velocity output.

from __future__ import annotations

import math

from pyglspg4.constants import CK2, CK4, AE


def apply_short_period(
    a: float,
    e: float,
    i: float,
    u: float,
    r: float,
    rdot: float,
    rfdot: float,
):
    """
    Apply short-period J2/J4 perturbations.

    Inputs:
        a     semi-major axis [Earth radii]
        e     eccentricity
        i     inclination [rad]
        u     argument of latitude [rad]
        r     radius [Earth radii]
        rdot  radial velocity [Earth radii/min]
        rfdot transverse velocity [Earth radii/min]

    Returns:
        corrected (r, rdot, rfdot, u)
    """

    sin_i = math.sin(i)
    cos_i = math.cos(i)
    sin_u = math.sin(u)
    cos_u = math.cos(u)

    sin2u = 2.0 * sin_u * cos_u
    cos2u = 2.0 * cos_u * cos_u - 1.0

    theta2 = cos_i * cos_i

    # ---- J2 short-period terms ----
    temp1 = CK2 / (r * r)
    temp2 = temp1 / (a * a)

    dr = -temp1 * (1.0 - 3.0 * theta2) * cos2u
    du = temp2 * sin2u * (1.0 - 3.0 * theta2)
    drdot = temp2 * sin2u * (1.0 - 3.0 * theta2) * rdot
    drfdot = -temp2 * (1.0 - 3.0 * theta2) * cos2u * rfdot

    # ---- J4 corrections (small but required) ----
    temp3 = CK4 / (r ** 4)

    dr += temp3 * (3.0 - 30.0 * theta2 + 35.0 * theta2 * theta2) * cos2u
    du += temp3 * sin2u * (3.0 - 30.0 * theta2 + 35.0 * theta2 * theta2)

    # ---- Apply corrections ----
    r += dr
    u += du
    rdot += drdot
    rfdot += drfdot

    return r, rdot, rfdot, u

