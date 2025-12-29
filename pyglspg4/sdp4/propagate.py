# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SDP-4 propagation dispatcher
#
# This module performs full deep-space propagation
# for satellites with orbital periods >= 225 minutes.
#
# References:
#   NORAD Spacetrack Report #3
#   Vallado et al., AIAA 2006-6753

from __future__ import annotations

import math
from typing import Tuple

from pyglspg4.constants import (
    AE,
    XKE,
    TWO_PI,
)
from pyglspg4.sgp4.state import SGP4State
from pyglspg4.sdp4.dspace import (
    deep_space_secular,
    deep_space_integrate,
)
from pyglspg4.math.vectors import teme_position_velocity


def propagate_deep_space(
    state: SGP4State,
    tsince_minutes: float,
) -> Tuple[
    Tuple[float, float, float],
    Tuple[float, float, float],
    int,
]:
    """
    Propagate a deep-space satellite using SDP-4.

    Parameters
    ----------
    state : SGP4State
        Initialized SGP-4 state with deep-space parameters
    tsince_minutes : float
        Minutes since TLE epoch

    Returns
    -------
    position_km : (x, y, z)
        TEME position vector (km)
    velocity_km_s : (vx, vy, vz)
        TEME velocity vector (km/s)
    error_code : int
        SDP-4 error code
    """

    # ------------------------------------------------------------------
    # 1. Apply deep-space secular effects
    # ------------------------------------------------------------------
    deep_space_secular(state, tsince_minutes)

    # ------------------------------------------------------------------
    # 2. Apply deep-space resonance integration
    # ------------------------------------------------------------------
    deep_space_integrate(state, tsince_minutes)

    # ------------------------------------------------------------------
    # 3. Solve Kepler's Equation
    # ------------------------------------------------------------------
    M = state.mean_anomaly % TWO_PI
    E = M

    for _ in range(10):
        f = E - state.eccentricity * math.sin(E) - M
        fp = 1.0 - state.eccentricity * math.cos(E)
        E -= f / fp

    sinE = math.sin(E)
    cosE = math.cos(E)

    beta = math.sqrt(1.0 - state.eccentricity ** 2)
    r = state.semi_major_axis * (1.0 - state.eccentricity * cosE)

    # ------------------------------------------------------------------
    # 4. Position and velocity in orbital plane
    # ------------------------------------------------------------------
    x_orb = state.semi_major_axis * (cosE - state.eccentricity)
    y_orb = state.semi_major_axis * beta * sinE

    rdot = XKE * math.sqrt(state.semi_major_axis) * state.eccentricity * sinE / r
    rfdot = XKE * math.sqrt(state.semi_major_axis) * beta / r

    vx_orb = -rdot * sinE + rfdot * cosE
    vy_orb = rdot * cosE + rfdot * sinE

    # ------------------------------------------------------------------
    # 5. Rotate into TEME frame
    # ------------------------------------------------------------------
    position, velocity = teme_position_velocity(
        x_orb,
        y_orb,
        vx_orb,
        vy_orb,
        state.inclination,
        state.raan,
        state.arg_perigee,
    )

    # ------------------------------------------------------------------
    # 6. Convert to physical units
    # ------------------------------------------------------------------
    position_km = tuple(p * AE for p in position)
    velocity_km_s = tuple(v * AE / 60.0 for v in velocity)

    return position_km, velocity_km_s, 0

