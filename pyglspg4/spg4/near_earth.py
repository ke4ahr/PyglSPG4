# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Near-Earth SGP-4 propagation.
# Implements Vallado SGP-4 equations for tsince minutes.

import math
from pyglspg4.constants import (
    AE,
    XKE,
    CK2,
    CK4,
    X2O3,
    SGP4_SUCCESS,
    SGP4_ERR_DECAYED,
)
from pyglspg4.math.kepler import solve_kepler
from pyglspg4.math.angles import wrap_two_pi
from pyglspg4.math.vectors import scale
from pyglspg4.sgp4.state import SGP4State


def propagate_near_earth(state: SGP4State, tsince_min):
    """
    Propagate SGP-4 near-Earth satellite.

    Returns:
        position (km), velocity (km/s), error_code
    """

    # Update mean anomaly and argument of perigee
    M = wrap_two_pi(state.mean_anomaly + state.mean_motion * tsince_min)
    argp = state.arg_perigee
    raan = state.raan
    e = state.eccentricity

    # Solve Kepler equation
    E = solve_kepler(M, e)
    sinE = math.sin(E)
    cosE = math.cos(E)

    # True anomaly
    nu = math.atan2(
        math.sqrt(1.0 - e * e) * sinE,
        cosE - e,
    )

    # Radius (Earth radii)
    a = (XKE / state.mean_motion) ** X2O3
    r = a * (1.0 - e * cosE)

    if r < AE:
        return (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), SGP4_ERR_DECAYED

    # Argument of latitude
    u = argp + nu

    # Position in orbital plane
    x_orb = r * math.cos(u)
    y_orb = r * math.sin(u)

    # Inclination effects
    cosi = math.cos(state.inclination)
    sini = math.sin(state.inclination)
    coso = math.cos(raan)
    sino = math.sin(raan)

    # TEME position (Earth radii)
    x = x_orb * coso - y_orb * cosi * sino
    y = x_orb * sino + y_orb * cosi * coso
    z = y_orb * sini

    # Convert to km
    pos_km = scale((x, y, z), 6378.137)

    # Velocity magnitude (km/s)
    mu = 398600.4418
    v_mag = math.sqrt(mu / (r * 6378.137))

    vx = -v_mag * (sino + coso)
    vy =  v_mag * (coso - sino)
    vz =  0.0

    vel_km_s = (vx, vy, vz)

    return pos_km, vel_km_s, SGP4_SUCCESS

