# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SDP-4 resonance initialization and handling
# Corresponds to NORAD dsinit and resonance logic
# References:
#   - Spacetrack Report #3
#   - Vallado et al. (2006), Sections 6–7

from __future__ import annotations

import math

from pyglspg4.sdp4.constants import (
    THDT,
    ROOT22,
    ROOT32,
    ROOT44,
    ROOT52,
    ROOT54,
)
from pyglspg4.sdp4.state import SDP4State


def initialize_resonance(state: SDP4State) -> None:
    """
    Initialize deep-space resonance terms.

    Handles:
      - Synchronous (1:1 Earth rotation)
      - 12-hour (Molniya) resonance
    """

    # Mean motion [rad/min]
    n = state.mean_motion

    # Detect synchronous resonance (~1 rev/day)
    if abs(n - THDT) < 1e-6:
        state.resonance = True
        state.synchronous = True

        state.del1 = ROOT22
        state.del2 = ROOT32
        state.del3 = ROOT44
        state.fasx2 = 0.13130908
        state.fasx4 = 2.8843198
        state.fasx6 = 0.37448087

    # Detect 12-hour resonance (~2 rev/day)
    elif abs(n - 2.0 * THDT) < 1e-6:
        state.resonance = True
        state.synchronous = False

        state.del1 = ROOT52
        state.del2 = ROOT54
        state.del3 = 0.0
        state.fasx2 = 0.0
        state.fasx4 = 0.0
        state.fasx6 = 0.0

    else:
        state.resonance = False
        state.synchronous = False

    # Initialize integration variables
    state.atime = 0.0
    state.xli = state.mean_anomaly
    state.xni = state.mean_motion

