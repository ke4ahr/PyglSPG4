# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Near-Earth SGP-4 propagation (period < 225 minutes).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from pyglspg4.constants import (
    J2,
    KE,
    EARTH_RADIUS_KM,
    TWO_PI,
    SECONDS_PER_DAY,
)
from pyglspg4.backend.base import MathBackend
from pyglspg4.math.numerics import solve_kepler
from pyglspg4.math.rotations import rotate_x, rotate_z
from pyglspg4.sgpsg4.state import SGP4State
from pyglspg4.api.exceptions import PropagationError


@dataclass(frozen=True)
class PositionVelocity:
    """
    Earth-centered inertial position and velocity.
    """
    position_km: tuple[float, float, float]
    velocity_km_s: tuple[float, float, float]


def propagate_near_earth(
    state: SGP4State,
    tsince_minutes: float,
    backend: MathBackend,
) -> PositionVelocity:
    """
    Propagate a near-Earth orbit using SGP-4.
    """

    # Unpack state
    n0 = state.mean_motion
    e0 = state.eccentricity
    i0 = state.inclination
    omega0 = state.argument_of_perigee
    raan0 = state.raan
    m0 = state.mean_anomaly
    bstar = state.bstar

    # Secular effects
    a0 = (KE / n0) ** (2.0 / 3.0)
    cos_i = backend.cos(i0)
    theta2 = cos_i * cos_i
    beta2 = 1.0 - e0 * e0
    beta = backend.sqrt(beta2)

    # Secular rates
    temp = 1.5 * J2 * (EARTH_RADIUS_KM ** 2) / (a0 * a0 * beta2 * beta)
    mdot = n0 + temp * (1.0 - 1.5 * theta2)
    argpdot = temp * (2.0 - 2.5 * theta2)
    raandot = -temp * cos_i

    # Updated elements
    m = m0 + mdot * tsince_minutes
    omega = omega0 + argpdot * tsince_minutes
    raan = raan0 + raandot * tsince_minutes

    # Atmospheric drag (simple SGP-4 drag model)
    drag = bstar * tsince_minutes
    a = a0 * (1.0 - drag)
    e = e0 - drag * 1e-4
    if e < 0.0:
        raise PropagationError("Eccentricity became negative")

    # Kepler equation
    E = solve_kepler(m % TWO_PI, e, backend)

    sinE = backend.sin(E)
    cosE = backend.cos(E)

    # True anomaly
    nu = backend.atan2(
        backend.sqrt(1.0 - e * e) * sinE,
        cosE - e,
    )

    # Distance
    r = a * (1.0 - e * cosE)

    # Position in orbital plane
    x_orb = r * backend.cos(nu)
    y_orb = r * backend.sin(nu)

    # Velocity in orbital plane
    p = a * (1.0 - e * e)
    h = backend.sqrt(KE * EARTH_RADIUS_KM *

