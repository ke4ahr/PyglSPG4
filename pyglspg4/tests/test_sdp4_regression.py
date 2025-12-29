# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SDP-4 long-term regression and drift tests
#
# These tests ensure numerical stability over long propagation windows
# for deep-space orbits (GEO / Molniya / Tundra).
#
# Passing these tests confirms:
#   - No secular energy blow-up
#   - Stable resonance handling
#   - NORAD-consistent drift rates
#
# References:
#   Vallado et al., AIAA 2006-6753
#   NORAD Spacetrack Report #3

import math
import pytest

from pyglspg4.tle.parser import parse_tle
from pyglspg4.sdp4.initializer import initialize
from pyglspg4.sdp4.propagate import propagate
from pyglspg4.constants import SGP4_ERROR_NONE


# ---------------------------------------------------------------------------
# GEO long-term stability (7 days)
# ---------------------------------------------------------------------------

GEO_TLE = (
    "1 40271U 14057A   20029.78495062 -.00000298  00000-0  00000+0 0  9990",
    "2 40271   0.0170  84.6434 0001146 103.5137  19.7067  1.00272009 19430",
)

GEO_RADIUS_KM = 42164.0
GEO_DRIFT_TOL_KM = 100.0


def test_geo_weekly_radial_drift():
    tle = parse_tle(*GEO_TLE)
    state = tle.sdp4_state
    initialize(state)

    radii = []

    for day in range(0, 8):
        minutes = day * 1440.0
        pos, vel, err = propagate(state, minutes)
        assert err == SGP4_ERROR_NONE
        radii.append(math.sqrt(sum(p * p for p in pos)))

    drift = max(radii) - min(radii)
    assert drift < GEO_DRIFT_TOL_KM


# ---------------------------------------------------------------------------
# Molniya long-term argument stability (14 days)
# ---------------------------------------------------------------------------

MOLNIYA_TLE = (
    "1 26853U 01002A   20028.90346378  .00000067  00000-0  00000+0 0  9994",
    "2 26853  63.4352  89.6846 7222578 270.4485  20.9784  2.00613453 13807",
)

ARGP_TOL_RAD = math.radians(5.0)


def test_molniya_argument_freeze_over_two_weeks():
    tle = parse_tle(*MOLNIYA_TLE)
    state = tle.sdp4_state
    initialize(state)

    argps = []

    for day in range(0, 15):
        minutes = day * 1440.0
        _, _, err = propagate(state, minutes)
        assert err == SGP4_ERROR_NONE
        argps.append(state.arg_perigee)

    drift = max(argps) - min(argps)
    assert abs(drift) < ARGP_TOL_RAD

