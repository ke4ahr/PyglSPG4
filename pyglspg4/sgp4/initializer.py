# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
SGP-4 initializer.

Transforms parsed TLE elements into normalized SGP-4 state parameters
and determines whether the satellite should be propagated using the
near-Earth (SGP-4) or deep-space (SDP-4) model.
"""

from __future__ import annotations

from dataclasses import dataclass

from pyglspg4.constants import PI, TWO_PI
from pyglspg4.sgp4.state import SGP4State


@dataclass(frozen=True)
class SGP4Initialization:
    """
    Results of SGP-4 initialization.
    """
    state: SGP4State
    mean_motion_rad_per_min: float
    is_deep_space: bool


def initialize_sgp4(parsed_tle) -> SGP4Initialization:
    """
    Initialize SGP-4 / SDP-4 from parsed TLE data.

    Args:
        parsed_tle: ParsedTLE instance

    Returns:
        SGP4Initialization structure.
    """

    # Convert angles to radians
    deg_to_rad = PI / 180.0

    inclination = parsed_tle.inclination_deg * deg_to_rad
    raan = parsed_tle.raan_deg * deg_to_rad
    argument_of_perigee = parsed_tle.argument_of_perigee_deg * deg_to_rad
    mean_anomaly = parsed_tle.mean_anomaly_deg * deg_to_rad

    # Mean motion: rev/day -> rad/min
    mean_motion_rad_per_min = (
        parsed_tle.mean_motion_rev_per_day * TWO_PI / 1440.0
    )

    state = SGP4State(
        mean_motion=mean_motion_rad_per_min,
        eccentricity=parsed_tle.eccentricity,
        inclination=inclination,
        argument_of_perigee=argument_of_perigee,
        raan=raan,
        mean_anomaly=mean_anomaly,
    )

    # Deep-space if orbital period >= 225 minutes
    period_minutes = TWO_PI / mean_motion_rad_per_min
    is_deep_space = period_minutes >= 225.0

    return SGP4Initialization(
        state=state,
        mean_motion_rad_per_min=mean_motion_rad_per_min,
        is_deep_space=is_deep_space,
    )

