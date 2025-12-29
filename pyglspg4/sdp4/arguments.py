# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SDP-4 lunar / solar argument evolution
#
# This module computes the time-varying deep-space arguments:
#   - Mean longitude of the Sun
#   - Mean longitude of the Moon
#   - Solar / lunar node regressions
#
# Required for:
#   - GEO resonance
#   - Molniya resonance
#   - Correct long-term drift
#
# References:
#   Spacetrack Report #3
#   Vallado et al., AIAA 2006-6753 §7.3

from __future__ import annotations

import math
from pyglspg4.sdp4.state import SDP4State

TWOPI = 2.0 * math.pi


def update_lunar_solar_arguments(state: SDP4State, tsince_minutes: float) -> None:
    """
    Update solar and lunar arguments for deep-space propagation.

    Parameters
    ----------
    state : SDP4State
        Deep-space state (updated in place)
    tsince_minutes : float
        Minutes since epoch
    """

    # Time in Julian centuries
    t = tsince_minutes / 525600.0

    # Mean longitude of the Sun
    state.solar_longitude = (
        4.8950630 + 628.331966786 * t
    ) % TWOPI

    # Mean longitude of the Moon
    state.lunar_longitude = (
        4.7199672 + 8399.7091449254 * t
    ) % TWOPI

    # Lunar ascending node
    state.lunar_node = (
        5.8351514 - 33.321672156 * t
    ) % TWOPI

    # Solar node (fixed in SDP-4)
    state.solar_node = 0.0

