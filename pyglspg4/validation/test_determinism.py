# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Determinism and thread-safety validation for SGP-4 / SDP-4
#
# These tests ensure propagation results are repeatable,
# independent of call order or execution context.

from __future__ import annotations

import math

from pyglspg4.tle.parser import parse_tle
from pyglspg4.sgp4.initializer import initialize
from pyglspg4.sgp4.propagate import propagate


def _vec_equal(a, b, tol=1e-12):
    for i in range(3):
        if abs(a[i] - b[i]) > tol:
            return False
    return True


def test_repeatability_near_earth() -> None:
    """
    Running propagation multiple times with the same
    inputs must yield identical results.
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

    tsince = 123.456

    r1, v1, e1 = propagate(state, tsince)
    r2, v2, e2 = propagate(state, tsince)

    assert e1 == 0
    assert e2 == 0

    assert _vec_equal(r1, r2)
    assert _vec_equal(v1, v2)


def test_multiple_calls_no_state_drift() -> None:
    """
    Repeated calls must not accumulate error due to
    hidden mutation of the state object.
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

    tsince = 10.0

    ref_r, ref_v, _ = propagate(state, tsince)

    for _ in range(50):
        r, v, err = propagate(state, tsince)
        assert err == 0
        assert _vec_equal(r, ref_r)
        assert _vec_equal(v, ref_v)


def test_finite_outputs_all_times() -> None:
    """
    No NaNs or infinities may appear during normal propagation.
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

    for tsince in range(-1440, 1440, 60):
        r, v, err = propagate(state, float(tsince))
        assert err == 0
        for i in range(3):
            assert math.isfinite(r[i])
            assert math.isfinite(v[i])

