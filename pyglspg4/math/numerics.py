# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Numerical solvers.
"""

from __future__ import annotations

from pyglspg4.api.exceptions import ConvergenceError
from pyglspg4.constants import KEPLER_EPSILON, MAX_KEPLER_ITERATIONS


def solve_kepler(mean_anomaly: float, eccentricity: float, backend) -> float:
    """
    Solve Kepler's equation for eccentric anomaly using Newton-Raphson.

    This solver is bounded and deterministic.
    """
    e = eccentricity
    m = mean_anomaly

    if e < 1e-8:
        return m

    E = m
    for _ in range(MAX_KEPLER_ITERATIONS):
        f = E - e * backend.sin(E) - m
        f_prime = 1.0 - e * backend.cos(E)
        delta = -f / f_prime
        E += delta
        if backend.abs(delta) < KEPLER_EPSILON:
            return E

    raise ConvergenceError("Kepler solver failed to converge")

