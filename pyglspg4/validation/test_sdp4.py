# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Unit tests for SDP-4 deep-space propagation
#
# These tests verify correct execution of the deep-space
# propagation path, including resonance handling and
# long-term numerical stability.
#
# References:
#   Vallado et al., AIAA 2006-6753

from __future__ import annotations

import math

from pyglspg4.tle.parser import parse_tle
from pyglspg4.sgp4.initializer import initialize
from pyglspg4.sgp4.propagate import propagate


def test_sdp4_executes_without_error() -> None:
    """
    Ensure SDP-4 deep-space propagation executes and
    produces finite results for a GEO-class orbit.
    """

    # Example GEO TLE (public test satellite)
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

    assert state.is_deep_space is True

    # Propagate over several days
    for tsince in range(0, 1440 * 7, 720):  # minutes
        r, v, err = propagate(state, float(tsince))

        assert err == 0

        for i in range(3):
            assert math.isfinite(r[i])
            assert math.isfinite(v[i])

