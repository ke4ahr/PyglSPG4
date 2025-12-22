# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
SGP-4 near-Earth propagator.

Implements a simplified, thread-safe near-Earth SGP-4 propagation
path suitable for orbits with periods less than 225 minutes.

NOTE:
This implementation currently provides a *minimal* Keplerian
propagation scaffold. Full SGP-4 perturbation terms (J2 drag,
secular and periodic corrections) are intentionally staged for
incremental implementation.
"""

from __future__ import annotations

from dataclasses import dataclass

from pyglspg4.backend.base import MathBackend
from pyglspg4.math.numerics import solve_kepler
from pyglspg4.math.rotations import rotate_x, rotate_z
from pyglspg4.math.vectors import norm
from pyglspg4.constants import KE


@dataclass(frozen=True)
class PositionVelocity:
    """
    Immutable position/velocity container.
    """
    position_km: tuple[float, float, float]
    velocity_km_s: tuple[float, float, float]


def propagate_near_earth(state, tsince_minutes: float, backend: MathBackend):
    """
    Propagate a near-Earth orbit using a simplified SGP-4 model.

    Args:
        state: SGP4State
        tsince_minutes: Time since epoch (minutes)
        backend: MathBackend

    Returns:
        PositionVelocity object
    """

    # Mean anomaly update
    M = state.mean_anomaly + state.mean_motion * tsince_minutes

    # Solve Kepler equation
    E = solve_kepler(M, state.eccentricity, backend)

    # True anomaly
    sin_v = (
        backend.sqrt(1.0 - state.eccentricity ** 2)
        * backend.sin(E)
        / (1.0 - state.eccentricity * backend.cos(E))
    )
    cos_v = (
        backend.cos(E) - state.eccentricity
    ) / (1.0 - state.eccentricity * backend.cos(E))

    v = backend.atan2(sin_v, cos_v)

    # Radius (Earth radii)
    r = (
        KE ** (2.0 / 3.0)
        / (state.mean_motion ** (2.0 / 3.0))
        * (1.0 - state.eccentricity * backend.cos(E))
    )

    # Position in orbital plane
    x_orb = r * cos_v
    y_orb = r * sin_v
    z_orb = 0.0

    # Rotate into ECI frame
    v1 = rotate_z((x_orb, y_orb, z_orb), state.argument_of_perigee, backend)
    v2 = rotate_x(v1, state.inclination, backend)
    pos = rotate_z(v2, state.raan, backend)

    # Velocity magnitude (simplified vis-viva)
    mu = 1.0  # normalized gravitational parameter
    v_mag = backend.sqrt(mu * (2.0 / r - 1.0 / (r / (1.0 - state.eccentricity))))

    # Directional velocity (tangential approximation)
    vel = (
        -v_mag * backend.sin(v),
        v_mag * backend.cos(v),
        0.0,
    )

    return PositionVelocity(
        position_km=pos,
        velocity_km_s=vel,
    )

