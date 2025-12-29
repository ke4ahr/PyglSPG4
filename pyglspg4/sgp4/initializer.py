# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SGP-4 initialization logic
#
# This module performs the full SGP-4 initialization sequence
# as defined in NORAD Spacetrack Report #3 and Vallado (AIAA 2006-6753).
#
# Responsibilities:
#   - Convert TLE elements into internal SGP-4 state
#   - Compute derived constants
#   - Apply near-Earth vs deep-space classification
#   - Prepare all coefficients required for propagation
#
# This file must be executed exactly once per TLE before propagation.

from __future__ import annotations

import math

from pyglspg4.constants import (
    AE,
    XKE,
    CK2,
    CK4,
    QOMS2T,
    S,
    TWO_PI,
)
from pyglspg4.sgp4.state import SGP4State


def initialize(state: SGP4State) -> None:
    """
    Initialize an SGP-4 state from parsed TLE data.

    Parameters
    ----------
    state : SGP4State
        State object populated with raw TLE values.
        Modified in-place.
    """

    # ------------------------------------------------------------------
    # 1. Recover original mean motion and semi-major axis
    # ------------------------------------------------------------------
    state.a1 = (XKE / state.mean_motion) ** (2.0 / 3.0)

    cosi0 = math.cos(state.inclination)
    theta2 = cosi0 * cosi0

    beta0 = math.sqrt(1.0 - state.eccentricity ** 2)
    temp = (1.5 * CK2 * (3.0 * theta2 - 1.0)) / (beta0 ** 3)

    state.del1 = temp / (state.a1 ** 2)
    state.a0 = state.a1 * (1.0 - state.del1 * (0.5 * (2.0 / 3.0) +
                                               state.del1 * (1.0 +
                                               134.0 / 81.0 * state.del1)))

    state.del0 = temp / (state.a0 ** 2)
    state.mean_motion = state.mean_motion / (1.0 + state.del0)

    state.semi_major_axis = state.a0

    # ------------------------------------------------------------------
    # 2. Perigee and atmospheric parameters
    # ------------------------------------------------------------------
    perigee_km = (state.semi_major_axis * (1.0 - state.eccentricity) - AE) * AE

    if perigee_km < 156.0:
        state.s = max(perigee_km - 78.0, 20.0)
        state.qoms2t = ((120.0 - state.s) * AE) ** 4
        state.s = state.s / AE + AE
    else:
        state.s = S
        state.qoms2t = QOMS2T

    # ------------------------------------------------------------------
    # 3. Drag-related coefficients
    # ------------------------------------------------------------------
    pinvsq = 1.0 / (state.semi_major_axis ** 2 * beta0 ** 4)

    tsi = 1.0 / (state.semi_major_axis - state.s)
    eta = state.semi_major_axis * state.eccentricity * tsi
    etasq = eta * eta
    eeta = state.eccentricity * eta

    psisq = abs(1.0 - etasq)
    coef = state.qoms2t * tsi ** 4
    coef1 = coef / (psisq ** 3.5)

    state.cc2 = (
        coef1 * state.mean_motion *
        (state.semi_major_axis *
         (1.0 + 1.5 * etasq + eeta * (4.0 + etasq)) +
         0.75 * CK2 * tsi / psisq *
         (3.0 * theta2 - 1.0) *
         (8.0 + 3.0 * etasq * (8.0 + etasq)))
    )

    state.cc1 = state.bstar * state.cc2

    # ------------------------------------------------------------------
    # 4. Secular rates
    # ------------------------------------------------------------------
    state.xmdot = (
        state.mean_motion +
        0.5 * temp * beta0 * state.mean_motion
    )

    state.omgdot = (
        -0.5 * temp * (1.0 - 5.0 * theta2)
    )

    state.xnodot = (
        -temp * cosi0
    )

    # ------------------------------------------------------------------
    # 5. Higher-order drag terms
    # ------------------------------------------------------------------
    if state.eccentricity > 1e-4:
        state.cc3 = (
            -2.0 * coef * tsi * CK2 *
            state.mean_motion * math.sin(state.arg_perigee) /
            state.eccentricity
        )
    else:
        state.cc3 = 0.0

    state.cc4 = (
        2.0 * state.mean_motion * coef1 *
        state.semi_major_axis * beta0 ** 2 *
        (eta * (2.0 + 0.5 * etasq) +
         state.eccentricity * (0.5 + 2.0 * etasq) -
         CK2 * tsi / (state.semi_major_axis * psisq) *
         (3.0 * theta2 - 1.0) *
         (8.0 + 3.0 * etasq * (8.0 + etasq)))
    )

    state.cc5 = (
        2.0 * coef1 * state.semi_major_axis * beta0 ** 2 *
        (1.0 + 2.75 * (etasq + eeta) + eeta * etasq)
    )

    # ------------------------------------------------------------------
    # 6. Final normalization
    # ------------------------------------------------------------------
    state.mean_anomaly %= TWO_PI
    state.arg_perigee %= TWO_PI
    state.raan %= TWO_PI

    state.initialized = True

