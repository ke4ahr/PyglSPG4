# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Numerical solvers and utilities.

Contains a robust, bounded Kepler equation solver used by both
SGP-4 and SDP-4 propagation paths.
"""

from __future__ import annotations

from pyglspg4.constants import KEPLER_EPSILON, MAX_KEPLER_ITERATIONS


class ConvergenceError(RuntimeError):
    """
    Raised when a numerical solver fails to converge within bounds.
    """
    pass


def solve_kepler(mean_anomaly: float, eccentricity: float, backend) -> float:
    """
    Solve Kepler's equation:

        E - e * sin(E) = M

    using a bounded Newton-Raphson iteration.

    Args:
        mean_anomaly: Mean anomaly M (radians)
        eccentricity: Orbital eccentricity e
        backend: MathBackend providing sin, cos, abs

    Returns:
        Eccentric anomaly E (radians)

    Raises:
        ConvergenceError if the solver does not converge.
    """
    if eccentricity < 1.0e-8:
        return mean_anomaly

    E = mean_anomaly
    for _ in range(MAX_KEPLER_ITERATIONS):
        f = E - eccentricity * backend.sin(E) - mean_anomaly
        f_prime = 1.0 - eccentricity * backend.cos(E)
        delta = -f / f_prime
        E += delta
        if backend.abs(delta) < KEPLER_EPSILON:
            return E

    raise ConvergenceError("Kepler solver failed to converge")

