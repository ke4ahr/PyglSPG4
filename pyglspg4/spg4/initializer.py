# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SGP-4 initialization logic.
# Computes coefficients and flags from TLE data.

import math
from pyglspg4.constants import (
    AE,
    XKE,
    CK2,
    CK4,
    QOMS2T,
    S,
    X2O3,
)
from pyglspg4.sgp4.state import SGP4State
from pyglspg4.math.angles import wrap_two_pi


def initialize_sgp4(tle):
    """
    Initialize SGP-4 state from parsed TLE.
    """

    # Convert angles to radians
    incl = math.radians(tle.inclination)
    raan = math.radians(tle.raan)
    argp = math.radians(tle.arg_perigee)
    mean_anom = math.radians(tle.mean_anomaly)

    # Mean motion in radians / minute
    n0 = tle.mean_motion * 2.0 * math.pi / 1440.0

    # Semi-major axis (Earth radii)
    a1 = (XKE / n0) ** X2O3
    cosio = math.cos(incl)
    theta2 = cosio * cosio

    eosq = tle.eccentricity * tle.eccentricity
    beta02 = 1.0 - eosq
    beta0 = math.sqrt(beta02)

    del1 = 1.5 * CK2 * (3.0 * theta2 - 1.0) / (beta0 ** 3 * a1 * a1)
    a0 = a1 * (1.0 - del1 * (0.5 * X2O3 + del1 * (1.0 + 134.0 / 81.0 * del1)))
    del0 = 1.5 * CK2 * (3.0 * theta2 - 1.0) / (beta0 ** 3 * a0 * a0)
    n0dp = n0 / (1.0 + del0)

    # Initialize state
    state = SGP4State(
        epoch_year=tle.epoch_year,
        epoch_day=tle.epoch_day,
        inclination=incl,
        raan=wrap_two_pi(raan),
        eccentricity=tle.eccentricity,
        arg_perigee=wrap_two_pi(argp),
        mean_anomaly=wrap_two_pi(mean_anom),
        mean_motion=n0dp,
        bstar=tle.bstar,
    )

    # Simple perigee check for atmospheric model
    perigee = (a0 * (1.0 - tle.eccentricity) - AE) * 6378.137
    if perigee < 220.0:
        state.isimp = 1

    # Drag coefficients
    s4 = S
    qoms24 = QOMS2T

    tsi = 1.0 / (a0 - s4)
    eta = a0 * tle.eccentricity * tsi
    eta2 = eta * eta
    psisq = abs(1.0 - eta2)

    coef = qoms24 * (tsi ** 4)
    coef1 = coef / (psisq ** 3.5)

    state.c2 = coef1 * n0dp * (
        a0 * (1.0 + 1.5 * eta2 + 4.0 * tle.eccentricity * eta + tle.eccentricity * eta2)
    )

    state.sinmao = math.sin(mean_anom)
    state.t2cof = 1.5 * state.c2
    state.omgcof = tle.bstar * coef * math.cos(argp)
    state.xmcof = -X2O3 * coef * tle.bstar / eta if abs(eta) > 1e-12 else 0.0

    return state

