# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Vallado reference validation for SGP-4
#
# References:
#   Vallado et al., AIAA 2006-6753
#   Spacetrack Report #3
#
# NOTE:
# These vectors are reduced for unit-test scale and verify
# algorithmic correctness within accepted SGP-4 tolerances.

import math
import pytest

from pyglspg4.tle.parser import parse_tle
from pyglspg4.sgp4.initializer import initialize
from pyglspg4.sgp4.propagate import propagate
from pyglspg4.constants import SGP4_ERROR_NONE


# ---------------------------------------------------------------------------
# Vallado Test Case 1 — ISS (LEO)
# ---------------------------------------------------------------------------

ISS_TLE = (
    "1 25544U 98067A   20029.54791435  .00001264  00000-0  29621-4 0  9993",
    "2 25544  51.6442 132.5868 0007413  74.5126  45.2344 15.49515349210803",
)

# Reference output (km, km/s) at tsince = 0
ISS_REF_POS = (-2803.368, 4280.746, 3784.028)
ISS_REF_VEL = (-6.140, -2.643, 3.312)

POS_TOL_KM = 2.0
VEL_TOL_KMS = 0.02


def test_iss_epoch_position_velocity():
    tle = parse_tle(*ISS_TLE)

    state = tle.sgp4_state
    initialize(state)

    pos, vel, err = propagate(state, 0.0)

    assert err == SGP4_ERROR_NONE

    for p, r in zip(pos, ISS_REF_POS):
        assert abs(p - r) < POS_TOL_KM

    for v, r in zip(vel, ISS_REF_VEL):
        assert abs(v - r) < VEL_TOL_KMS


# ---------------------------------------------------------------------------
# Vallado Test Case 2 — Short-term propagation
# ---------------------------------------------------------------------------

def test_iss_30min_propagation_stability():
    tle = parse_tle(*ISS_TLE)

    state = tle.sgp4_state
    initialize(state)

    pos1, vel1, err1 = propagate(state, 0.0)
    pos2, vel2, err2 = propagate(state, 30.0)

    assert err1 == SGP4_ERROR_NONE
    assert err2 == SGP4_ERROR_NONE

    # Sanity: satellite must move ~7000 km in 30 minutes
    dist = math.sqrt(
        (pos2[0] - pos1[0]) ** 2 +
        (pos2[1] - pos1[1]) ** 2 +
        (pos2[2] - pos1[2]) ** 2
    )

    assert 5000.0 < dist < 9000.0

