# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Validation checks for parsed TLE data.
# Ensures values are within physically meaningful bounds.

import math
from pyglspg4.tle.parser import TLE


def validate_tle(tle: TLE):
    """
    Validate TLE fields for basic physical correctness.
    Raises ValueError on invalid data.
    """

    if not (0.0 <= tle.eccentricity < 1.0):
        raise ValueError("Eccentricity out of range")

    if not (0.0 <= tle.inclination <= 180.0):
        raise ValueError("Inclination out of range")

    if tle.mean_motion <= 0.0:
        raise ValueError("Mean motion must be positive")

    for angle_name, angle in (
        ("RAAN", tle.raan),
        ("Argument of perigee", tle.arg_perigee),
        ("Mean anomaly", tle.mean_anomaly),
    ):
        if not (0.0 <= angle < 360.0):
            raise ValueError(f"{angle_name} out of range")

    if abs(tle.bstar) > 1.0:
        raise ValueError("BSTAR magnitude unreasonably large")

    return True

