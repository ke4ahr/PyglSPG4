# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SDP-4 deep-space periodic perturbations (dpper)
# Full harmonic expansion per NORAD Spacetrack Report #3
#
# References:
#   Vallado et al., AIAA 2006-6753, Section 7.4

from __future__ import annotations

import math

from pyglspg4.sdp4.state import SDP4State


def dpper(state: SDP4State, tsince: float) -> None:
    """
    Apply deep-space periodic perturbations.

    Updates orbital elements in-place:
      - eccentricity
      - inclination
      - argument of perigee
      - mean anomaly
      - RAAN
    """

    # --- Long-period corrections ---
    pe = state.pe
    pinc = state.pinc
    pl = state.pl
    pgh = state.pgh
    ph = state.ph

    # --- Inclination singularity handling ---
    sin_inc = math.sin(state.inclination)
    if abs(sin_inc) < 1e-6:
        ph = 0.0
    else:
        ph /= sin_inc

    # --- Apply corrections ---
    state.eccentricity += pe
    state.inclination += pinc

    state.mean_anomaly += pl
    state.arg_perigee += pgh
    state.raan += ph

    # --- Normalize angles ---
    twopi = 2.0 * math.pi
    state.mean_anomaly %= twopi
    state.arg_perigee %= twopi
    state.raan %= twopi

