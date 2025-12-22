# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
SGP-4 initialization routines.

Converts parsed TLE data into normalized SGP-4 internal state.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from pyglspg4.constants import (
    PI,
    TWO_PI,
    KE,
    EARTH_RADIUS_KM,
    J2,
)
from pyglspg4.sgpsg4.state import SGP4State
from pyglspg4.tle.parser import ParsedTLE


@dataclass(frozen=True)
class InitializedSGP4:
    """
    Fully initialized SGP-4 internal parameters.

    Immutable and thread-safe.
    """
    state: SGP4State
    semi_major_axis: float
    mean_motion_rad_per_min: float
    is_deep_space: bool


def initialize_sgp4(tle: ParsedTLE) -> InitializedSGP4:
    """
    Initialize SGP-4 from parsed TLE.

    This function performs unit conversion, normalization,
    and orbit regime classification.
    """

    # Epoch year normalization (TLE two-digit year)
    year = tle.epoch_year
    year += 2000 if year < 57 else 1900

    # Convert angles to radians
    inclination = math.radians(tle.inclination_deg)
    raan = math.radians(tle.raan_deg)
    argp = math.radians(tle.argument_of_perigee_deg)
    mean_anomaly = math.radians(tle.mean_anomaly_deg)

    # Mean motion conversion: rev/day -> rad/min
    mean_motion_rad_per_min = (
        tle.mean_motion_rev_per_day * TWO_PI / 1440.0
    )

    # Semi-major axis from mean motion (SGP-4 standard)
    a1 = (KE / mean_motion_rad_per_min) ** (2.0 / 3.0)
    cos_i = math.cos(inclination)
    theta2 = cos_i * cos_i
    x3thm1 = 3.0 * theta2 - 1.0
    e2 = tle.eccentricity * tle.eccentricity
    beta2 = 1.0 - e2
    beta = math.sqrt(beta2)

    del1 = (
        1.5 * J2 * x3thm1 / (a1 * a1 * beta * beta2)
    )
    a0 = a1 * (1.0 - del1 / 3.0 - del1 * del1 - (134.0 / 81.0) * del1 ** 3)

    del0 = (
        1.5 * J2 * x3thm1 / (a0 * a0 * beta * beta2)
    )

    mean_motion = mean_motion_rad_per_min / (1.0 + del0)

    semi_major_axis = a0 / (1.0 - del0)

    # Orbit period in minutes
    period_minutes = TWO_PI / mean_motion

    # Deep-space classification (>= 225 minutes)
    is_deep_space = period_minutes >= 225.0

    state = SGP4State(
        mean_motion=mean_motion,
        eccentricity=tle.eccentricity,
        inclination=inclination,
        argument_of_perigee=argp,
        raan=raan,
        mean_anomaly=mean_anomaly,
        bstar=tle.bstar,
    )

    return InitializedSGP4(
        state=state,
        semi_major_axis=semi_major_axis,
        mean_motion_rad_per_min=mean_motion,
        is_deep_space=is_deep_space,
    )

