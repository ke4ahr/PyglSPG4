# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Regression validation utilities.

Provides minimal, deterministic helpers for executing regression-style
checks against stored or known-good reference states. This module is
intended to support automated testing and continuous integration.
"""

from __future__ import annotations

from typing import Callable, Iterable, Tuple

from pyglspg4.validation.reference import ReferenceState, compare_states


def run_regression(
    cases: Iterable[Tuple[Callable[[], ReferenceState], ReferenceState]],
    position_tolerance_km: float,
    velocity_tolerance_km_s: float,
):
    """
    Run regression checks against a sequence of reference cases.

    Args:
        cases: Iterable of tuples:
               (callable returning computed ReferenceState,
                expected ReferenceState)
        position_tolerance_km: Maximum allowed absolute position error (km)
        velocity_tolerance_km_s: Maximum allowed absolute velocity error (km/s)

    Raises:
        AssertionError if any case exceeds tolerance.
    """

    for compute_fn, reference in cases:
        computed = compute_fn()
        pos_err, vel_err = compare_states(computed, reference)

        max_pos_err = max(abs(e) for e in pos_err)
        max_vel_err = max(abs(e) for e in vel_err)

        if max_pos_err > position_tolerance_km:
            raise AssertionError(
                f"Position regression failure: {max_pos_err} km > "
                f"{position_tolerance_km} km"
            )

        if max_vel_err > velocity_tolerance_km_s:
            raise AssertionError(
                f"Velocity regression failure: {max_vel_err} km/s > "
                f"{velocity_tolerance_km_s} km/s"
            )

