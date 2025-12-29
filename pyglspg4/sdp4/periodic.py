# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SDP-4 deep-space periodic perturbations
# Corresponds to NORAD dpper routine
# References:
#   - Spacetrack Report #3
#   - Vallado et al. (2006), Section 7

from __future__ import annotations

import math

from pyglspg4.sdp4.state import SDP4State


def apply_periodic(state: SDP4State) -> None:
    """
    Apply deep-space periodic corrections to orbital elements.

    Updates:
      - eccentricity
      - inclination
      - argument of perigee
      - mean anomaly
      - RAAN
    """

    # Apply periodic terms
    state.eccentricity += state.pe
    state.inclination += state.pinc

    state.mean_anomaly += state.pl
    state.arg_perigee += state.pgh
    state.raan += state.ph

    # Normalize angles
    state.mean_anomaly = state.mean_anomaly % (2.0 * math.pi)
    state.arg_perigee = state.arg_perigee % (2.0 * math.pi)
    state.raan = state.raan % (2.0 * math.pi)

