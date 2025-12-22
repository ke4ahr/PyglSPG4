# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Deep-space orbital-plane to ECI conversion.
"""

from __future__ import annotations

from pyglspg4.backend.base import MathBackend
from pyglspg4.math.numerics import solve_kepler
from pyglspg4.math.rotations import rotate_x, rotate_z
from pyglspg4.constants import KE, EARTH_RADIUS_KM
from pyglspg4.sdp4.state import SDP4State


def deep_space_eci(
    state: SDP4State,
    backend: MathBackend,
):
    """
    Compute ECI position and velocity for deep-space orbit.
    """

    a = (KE / state.mean_motion) ** (2.0 / 3.0)
    e = state.eccentricity

    E = solve_kepler(state.mean_anomaly, e, backend)
    sinE = backend.sin(E)
    cosE = backend.cos(E)

    nu = backend.atan2(
        backend.sqrt(1.0 - e * e) * sinE,
        cosE - e,
    )

    r = a * (1.0 - e * cosE)

    x_orb = r * backend.cos(nu)
    y_orb = r * backend.sin(nu)

    p = a * (1.0 - e * e)
    h = backend.sqrt(KE * EARTH_RADIUS_KM * p)

    vx_orb = -KE * EARTH_RADIUS_KM / h * backend.sin(nu)
    vy_orb = KE * EARTH_RADIUS_KM / h * (e + backend.cos(nu))

    r_vec = (x_orb, y_orb, 0.0)
    v_vec = (vx_orb, vy_orb, 0.0)

    r_vec = rotate_z(r_vec, state.argument_of_perigee, backend)
    r_vec = rotate_x(r_vec, state.inclination, backend)
    r_vec = rotate_z(r_vec, state.raan, backend)

    v_vec = rotate_z(v_vec, state.argument_of_perigee, backend)
    v_vec = rotate_x(v_vec, state.inclination, backend)
    v_vec = rotate_z(v_vec, state.raan, backend)

    v_vec = tuple(v / 60.0 for v in v_vec)

    return r_vec, v_vec

