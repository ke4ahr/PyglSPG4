# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SGP-4 near-Earth propagation logic
#
# This module implements the near-Earth (period < 225 minutes)
# secular and periodic perturbation model used by SGP-4.
#
# References:
#   NORAD Spacetrack Report #3
#   Vallado et al., AIAA 2006-6753

from __future__ import annotations

import math
from typing import Tuple

from pyglspg4.constants import (
    XKE,
    CK2,
    CK4,
    AE,
    TWO_PI,
)
from pyglspg4.sgp4.state import SGP4State
from pyglspg4.math.vectors import teme_position_velocity


def propagate_near_earth(
    state: SGP4State,
    tsince_minutes: float,
) -> Tuple[
    Tuple[float, float, float],
    Tuple[float, float, float],
    int,
]:
    """
    Propagate a near-Earth satellite using SGP-4.

    Parameters
    ----------
    state : SGP4State
        Initialized SGP-4 state
    tsince_minutes : float
        Minutes since TLE epoch

    Returns
    -------
    position_km : (x, y, z)
        TEME position vector (km)
    velocity_km_s : (vx, vy, vz)
        TEME velocity vector (km/s)
    error_code : int
        SGP4 error code
    """

    # ------------------------------------------------------------------
    # 1. Secular effects (drag, J2)
    # ------------------------------------------------------------------
    t = tsince_minutes

    state.mean_anomaly = (
        state.mean_anomaly +
        state.xmdot * t
    )

    state.arg_perigee = (
        state.arg_perigee +
        state.omgdot * t
    )

    state.raan = (
        state.raan +
        state.xnodot * t
    )

    # Drag terms
    tempa = 1.0 - state.cc1 * t
    tempe = state.bstar * state.cc4 * t
    templ = state.cc5 * t

    state.mean_anomaly += templ
    state.eccentricity -= tempe

    if state.eccentricity < 0.0:
        state.eccentricity = 0.0

    # ------------------------------------------------------------------
    # 2. Solve Kepler’s Equation
    # ------------------------------------------------------------------
    M = state.mean_anomaly % TWO_PI
    E = M
    for _ in range(10):
        f = E - state.eccentricity * math.sin(E) - M
        fp = 1.0 - state.eccentricity * math.cos(E)
        E -= f / fp

    sinE = math.sin(E)
    cosE = math.cos(E)

    # ------------------------------------------------------------------
    # 3. Position in orbital plane
    # ------------------------------------------------------------------
    beta = math.sqrt(1.0 - state.eccentricity ** 2)
    r = state.semi_major_axis * (1.0 - state.eccentricity * cosE)

    x_orb = state.semi_major_axis * (cosE - state.eccentricity)
    y_orb = state.semi_major_axis * beta * sinE

    # ------------------------------------------------------------------
    # 4. Velocity in orbital plane
    # ------------------------------------------------------------------
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
    # 6. Scale to physical units
    # ------------------------------------------------------------------
    position_km = tuple(p * AE for p in position)
    velocity_km_s = tuple(v * AE / 60.0 for v in velocity)

    # ------------------------------------------------------------------
    # 7. Normalize angles
    # ------------------------------------------------------------------
    state.mean_anomaly %= TWO_PI
    state.arg_perigee %= TWO_PI
    state.raan %= TWO_PI

    return position_km, velocity_km_s, 0

