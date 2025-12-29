# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Unit tests for SGP-4 propagation using Vallado reference vectors
#
# These tests verify numerical correctness of near-Earth SGP-4
# propagation against published reference data.
#
# References:
#   Vallado et al., AIAA 2006-6753

from __future__ import annotations

import math

from pyglspg4.tle.parser import parse_tle
from pyglspg4.sgp4.initializer import initialize
from pyglspg4.sgp4.propagate import propagate
from pyglspg4.validation.vallado_vectors import VALLADO_TEST_VECTORS


TOL_POS_KM = 1.0e-3      # 1 meter
TOL_VEL_KM_S = 1.0e-6    # 1 mm/s


def test_sgp4_against_vallado_vectors() -> None:
    """
    Validate SGP-4 propagation against Vallado reference vectors.
    """

    for vec in VALLADO_TEST_VECTORS:
        tle = parse_tle(vec.tle_line1, vec.tle_line2)
        state = initialize(tle)

        r, v, err = propagate(state, vec.tsince_minutes)

        assert err == 0

        for i in range(3):
            assert math.isclose(
                r[i],
                vec.position_km[i],
                abs_tol=TOL_POS_KM,
            ), f"Position mismatch axis {i}"

            assert math.isclose(
                v[i],
                vec.velocity_km_s[i],
                abs_tol=TOL_VEL_KM_S,
            ), f"Velocity mismatch axis {i}"

