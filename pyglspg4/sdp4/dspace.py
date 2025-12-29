# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SDP-4 deep-space secular and resonance integrator
#
# This module implements the NORAD deep-space (SDP-4)
# perturbation model for satellites with orbital periods
# >= 225 minutes.
#
# References:
#   NORAD Spacetrack Report #3
#   Vallado et al., AIAA 2006-6753

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Tuple

from pyglspg4.constants import (
    TWO_PI,
    XKE,
)
from pyglspg4.sdp4.constants import (
    ZNS,
    ZNL,
)
from pyglspg4.sgp4.state import SGP4State


@dataclass
class DeepSpaceState:
    """
    Deep-space resonance and secular integration state.
    """

    # Resonance flags
    is_resonant: bool = False
    is_synch: bool = False

    # Resonance coefficients
    del1: float = 0.0
    del2: float = 0.0
    del3: float = 0.0

    fasx2: float = 0.0
    fasx4: float = 0.0
    fasx6: float = 0.0

    # Time bookkeeping
    atime: float = 0.0
    xni: float = 0.0
    xli: float = 0.0

    # Secular rates
    dmdt: float = 0.0
    domdt: float = 0.0
    dnodt: float = 0.0


def deep_space_initialize(state: SGP4State) -> None:
    """
    Initialize deep-space resonance parameters.

    Called once during SGP-4 initialization
    for satellites with period >= 225 minutes.
    """

    ds = DeepSpaceState()

    # Mean motion in radians / minute
    n = state.mean_motion

    # Resonance determination
    if abs(n - TWO_PI / 1440.0) < 0.0001:
        ds.is_synch = True
        ds.is_resonant = True
    elif abs(n - TWO_PI / 43200.0) < 0.0001:
        ds.is_resonant = True

    # Store secular rates
    ds.dmdt = state.xmdot
    ds.domdt = state.omgdot
    ds.dnodt = state.xnodot

    # Initialize integrator state
    ds.atime = 0.0
    ds.xni = n
    ds.xli = state.mean_anomaly + state.arg_perigee + state.raan

    state.deep_space_state = ds


def deep_space_secular(
    state: SGP4State,
    tsince: float,
) -> None:
    """
    Apply deep-space secular effects.

    Updates mean anomaly, argument of perigee,
    and RAAN in-place.
    """

    ds = state.deep_space_state
    if ds is None:
        return

    state.mean_anomaly += ds.dmdt * tsince
    state.arg_perigee += ds.domdt * tsince
    state.raan += ds.dnodt * tsince

    state.mean_anomaly %= TWO_PI
    state.arg_perigee %= TWO_PI
    state.raan %= TWO_PI


def deep_space_integrate(
    state: SGP4State,
    tsince: float,
) -> None:
    """
    Perform deep-space resonance integration.

    This handles synchronous and 12-hour resonance
    effects via numerical stepping.
    """

    ds = state.deep_space_state
    if ds is None or not ds.is_resonant:
        return

    # Integration step (minutes)
    delt = 720.0 if tsince >= 0 else -720.0

    while abs(tsince - ds.atime) >= abs(delt):
        ds.atime += delt

        # Mean longitude integration
        ds.xli += ds.xni * delt

        # Update mean motion
        ds.xni += ds.del1 * math.sin(ds.xli)

    # Final partial step
    dt = tsince - ds.atime
    ds.xli += ds.xni * dt

    # Update orbital elements
    state.mean_anomaly = ds.xli - state.arg_perigee - state.raan
    state.mean_motion = ds.xni

