# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SDP-4 deep-space secular integrator
# Corresponds to NORAD dspace routine
# References:
#   - Spacetrack Report #3
#   - Vallado et al. (2006), Section 7

from __future__ import annotations

import math

from pyglspg4.sdp4.constants import (
    DEEP_SPACE_STEP,
    MAX_DEEP_STEPS,
)
from pyglspg4.sdp4.state import SDP4State


def integrate(state: SDP4State, tsince_minutes: float) -> None:
    """
    Integrate deep-space secular effects over time.

    This routine advances mean motion, mean anomaly, argument of perigee,
    and RAAN using resonance-aware numerical integration.
    """

    # No resonance → no deep-space integration needed
    if not state.resonance:
        return

    # Time difference from last integration
    delt = tsince_minutes - state.atime
    if delt == 0.0:
        return

    # Determine integration direction
    step = DEEP_SPACE_STEP if delt > 0.0 else -DEEP_SPACE_STEP

    # Integrate in steps
    steps = int(abs(delt) / abs(step)) + 1
    if steps > MAX_DEEP_STEPS:
        state.error = 1
        return

    for _ in range(steps):
        if abs(state.atime - tsince_minutes) < abs(step):
            step = tsince_minutes - state.atime

        # Update mean anomaly and mean motion
        state.xli += state.xni * step
        state.xni += (
            state.del1 * math.sin(state.fasx2 * state.atime)
            + state.del2 * math.sin(state.fasx4 * state.atime)
            + state.del3 * math.sin(state.fasx6 * state.atime)
        ) * step

        state.atime += step

    # Store results
    state.mean_anomaly = state.xli
    state.mean_motion = state.xni

