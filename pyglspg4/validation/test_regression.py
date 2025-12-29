# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Long-term regression tests for SGP-4 / SDP-4
#
# These tests ensure that propagated orbits remain
# physically reasonable over extended periods.
#
# This follows the validation philosophy described in:
#   Vallado, Fundamentals of Astrodynamics and Applications

from __future__ import annotations

import math

from pyglspg4.tle.parser import parse_tle
from pyglspg4.sgp4.initializer import initialize
from pyglspg4.sgp4.propagate import propagate


def _norm(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def test_leo_drag_decay() -> None:
    """
    A low Earth orbit with drag must show decreasing
    semi-major axis over time.
    """

    # ISS TLE (moderate drag)
    tle1 = (
        "1 25544U 98067A   20029.54791435  .00001264  00000-0  "
        "29621-4 0  9991"
    )
    tle2 = (
        "2 25544  51.6434  69.4038 0007414  74.5522  51.6356 "
        "15.49461746211616"
    )

    tle = parse_tle(tle1, tle2)
    state = initialize(tle)

    r0, _, _ = propagate(state, 0.0)
    r1, _, _ = propagate(state, 1440.0 * 3.0)  # 3 days

    assert _norm(r1) < _norm(r0)


def test_geo_orbit_stability() -> None:
    """
    GEO-class orbits should not decay significantly
    over several weeks.
    """

    tle1 = (
        "1 40294U 15037A   20029.12500000 -.00000260  00000-0  "
        "00000+0 0  9993"
    )
    tle2 = (
        "2 40294   0.0171  84.0035 0002030 107.3423 252.7554 "
        "1.00270000 16894"
    )

    tle = parse_tle(tle1, tle2)
    state = initialize(tle)

    r0, _, _ = propagate(state, 0.0)
    r1, _, _ = propagate(state, 1440.0 * 30.0)  # 30 days

    dr = abs(_norm(r1) - _norm(r0))

    # GEO radius should remain stable to within a few km
    assert dr < 10.0


def test_no_numerical_divergence() -> None:
    """
    No exponential growth or NaNs over long spans.
    """

    tle1 = (
        "1 25544U 98067A   20029.54791435  .00001264  00000-0  "
        "29621-4 0  9991"
    )
    tle2 = (
        "2 25544  51.6434  69.4038 0007414  74.5522  51.6356 "
        "15.49461746211616"
    )

    tle = parse_tle(tle1, tle2)
    state = initialize(tle)

    for day in range(0, 30):
        r, v, err = propagate(state, float(day * 1440))
        assert err == 0
        assert math.isfinite(_norm(r))
        assert math.isfinite(_norm(v))

