# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SGP-4 propagation dispatcher
#
# This module selects between near-Earth (SGP-4) and
# deep-space (SDP-4) propagation paths after initialization.
#
# References:
#   NORAD Spacetrack Report #3
#   Vallado et al., AIAA 2006-6753

from __future__ import annotations

from typing import Tuple

from pyglspg4.api.exceptions import SGP4PropagationError
from pyglspg4.sgp4.state import SGP4State
from pyglspg4.sgp4.near_earth import propagate_near_earth

# NOTE:
# Full SDP-4 deep-space propagation will dispatch here once
# pyglspg4.sdp4.propagate is finalized.
# from pyglspg4.sdp4.propagate import propagate_deep_space


def propagate(
    state: SGP4State,
    tsince_minutes: float,
) -> Tuple[
    Tuple[float, float, float],
    Tuple[float, float, float],
    int,
]:
    """
    Propagate a satellite using SGP-4 / SDP-4.

    Parameters
    ----------
    state : SGP4State
        Initialized SGP-4 state
    tsince_minutes : float
        Minutes since epoch (TLE epoch)

    Returns
    -------
    position_km : (x, y, z)
        TEME position vector in kilometers
    velocity_km_s : (vx, vy, vz)
        TEME velocity vector in kilometers per second
    error_code : int
        0 on success, non-zero on SGP-4 error
    """

    if not isinstance(state, SGP4State):
        raise TypeError("state must be an SGP4State")

    if not state.initialized:
        raise SGP4PropagationError("SGP4State has not been initialized")

    # Guard against nonsensical propagation
    if abs(tsince_minutes) > 1.0e8:

