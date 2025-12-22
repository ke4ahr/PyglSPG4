# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
ECI frame construction for SDP-4.

Provides helpers to construct Earth-Centered Inertial (ECI) position
and velocity vectors from deep-space orbital elements after secular
and periodic corrections have been applied.

This module mirrors the near-Earth ECI construction logic but is
kept separate to allow SDP-4–specific refinements.
"""

from __future__ import annotations

from pyglspg4.backend.base import MathBackend
from pyglspg4.math.rotations import rotate_x, rotate_z
from pyglspg4.math.numerics import solve_kepler
from pyglspg4.constants import KE


def elements_to_eci(
    mean_motion: float,
    eccentricity: float,
    inclination: float,
    argument_of_perigee: float,
    raan: float,
    mean_anomaly: float,
    backend: MathBackend,
):
    """
    Convert orbital elements to ECI position and velocity.

    Args:
        mean_motion: Mean motion (rad/min)
        eccentricity: Orbital eccentricity
        inclination: Inclination (rad)
        argument_of_perigee: Argument of perigee (rad)
        raan: Right ascension of ascending node (rad)
        mean_anomaly: Mean anomaly (rad)
        backend: MathBackend

    Returns:
        Tuple of:
            - position vector (km)
            - velocity vector (km/s)
    """

    # Solve Kepler equation
    E = solve_kepler(mean_anomaly, eccentricity, backend)

    # True anomaly
    sin_v = (
        backend.sqrt(1.0 - eccentricity ** 2)
        * backend.sin(E)
        / (1.0 - eccentricity * backend.cos(E))
    )
    cos_v = (
        backend.cos(E) - eccentricity
    ) / (1.0 - eccentricity * backend.cos(E))

    v = backend.atan2(sin_v, cos_v)

    # Radius (Earth radii)
    r = (
        KE ** (2.0 / 3.0)
        / (mean_motion ** (2.0 / 3.0))
        * (1.0 - eccentricity * backend.cos(E))
    )

    # Position in orbital plane
    x_orb = r * cos_v
    y_orb = r * sin_v
    z_orb = 0.0

    # Rotate into ECI frame
    v1 = rotate_z((x_orb, y_orb, z_orb), argument_of_perigee, backend)
    v2 = rotate_x(v1, inclination, backend)
    pos = rotate_z(v2, raan, backend)

    # Velocity (simplified, tangential approximation)
    mu = 1.0
    v_mag = backend.sqrt(mu * (2.0 / r - 1.0 / (r / (1.0 - eccentricity))))
    vel = (
        -v_mag * backend.sin(v),
        v_mag * backend.cos(v),
        0.0,
    )

    return pos, vel

