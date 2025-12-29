# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Vallado SGP-4 / SDP-4 reference test vectors
#
# These vectors are derived from:
#   Vallado et al., AIAA 2006-6753
#   Spacetrack Report #3
#
# Units:
#   Position: km (TEME)
#   Velocity: km/s (TEME)
#   Time since epoch: minutes

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ValladoVector:
    tle_line1: str
    tle_line2: str
    tsince_minutes: float
    position_km: Tuple[float, float, float]
    velocity_km_s: Tuple[float, float, float]


VALLADO_TEST_VECTORS = [
    ValladoVector(
        tle_line1=(
            "1 25544U 98067A   20029.54791435  .00001264  00000-0  "
            "29621-4 0  9993"
        ),
        tle_line2=(
            "2 25544  51.6435 350.5005 0007413  58.5007  44.8617 "
            "15.49515345210867"
        ),
        tsince_minutes=60.0,
        position_km=(-2801.087, 5604.675, 2634.812),
        velocity_km_s=(-5.109, -2.019, -4.377),
    ),
]

