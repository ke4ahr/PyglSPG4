# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Vallado reference validation for SDP-4 (deep-space)
#
# References:
#   Vallado et al., AIAA 2006-6753
#   NORAD Spacetrack Report #3
#
# These tests verify deep-space resonance behavior,
# secular drift, and long-term stability.

import math
import pytest

from pyglspg4.tle.parser import parse_tle
from pyglspg4.sdp4.initializer import initialize
from pyglspg4.sdp4.propagate import propagate
from pyglspg4.constants import SGP4_ERROR_NONE


# ---------------------------------------------------------------------------
# Vallado Test Case — GEO satellite
# ---------------------------------------------------------------------------

GEO_TLE = (
    "1 40271U 14057A   20029.78495062 -.00000298  00000-0  00000+0 0  9990",
    "2 40271   0.0170  84.6434 0001146 103.5137  19.7067  1.00272009 19430",
)

# Expected behavior:
# - Near-zero inclination
# - Semi-major axis ~42164 km
# - Very small radial drift over 24 hours

A_GEO_KM = 42164.0
A_TOL = 50.0


def test_geo_semi_major_axis_stability():
    tle = parse_tle(*GEO_TLE)
    state = tle.sdp4_state

    initialize(state)

    pos1, vel1, err1 = propagate(state, 0.0)
    pos2, vel2, err2 = propagate(state, 1440.0)  # +24 hours

    assert err1 == SGP4_ERROR_NONE
    assert err2 == SGP4_ERROR_NONE

    r1 = math.sqrt(sum(p * p for p in pos1))
    r2 = math.sqrt(sum(p * p for p in pos2))

    assert abs(r1 - A_GEO_KM) < A_TOL
    assert abs(r2 - A_GEO_KM) < A_TOL


# ---------------------------------------------------------------------------
# Vallado Test Case — Molniya orbit
# ---------------------------------------------------------------------------

MOLNIYA_TLE = (
    "1 26853U 01002A   20028.90346378  .00000067  00000-0  00000+0 0  9994",
    "2 26853  63.4352  89.6846 7222578 270.4485  20.9784  2.00613453

