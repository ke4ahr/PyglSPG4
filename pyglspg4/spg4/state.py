# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SGP-4 state container.
# Holds precomputed values used during propagation.

from dataclasses import dataclass


@dataclass
class SGP4State:
    # Epoch data
    epoch_year: int
    epoch_day: float

    # Mean elements (radians, Earth radii, minutes)
    inclination: float
    raan: float
    eccentricity: float
    arg_perigee: float
    mean_anomaly: float
    mean_motion: float

    # Drag terms
    bstar: float

    # Derived quantities (initialized later)
    isimp: int = 0
    aycof: float = 0.0
    xlcof: float = 0.0
    omgcof: float = 0.0
    xmcof: float = 0.0
    delmo: float = 0.0
    sinmao: float = 0.0
    t2cof: float = 0.0
    t3cof: float = 0.0
    t4cof: float = 0.0
    t5cof: float = 0.0

