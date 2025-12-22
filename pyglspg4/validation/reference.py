# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Reference validation scaffolding.

Provides structures and helpers for validating Pyglspg4 propagation
results against trusted reference implementations (e.g., Vallado SGP4,
Celestrak test vectors).

This module is intentionally lightweight and deterministic, serving
as an integration point for regression testing rather than a full
test harness.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ReferenceState:
    """
    Immutable reference state snapshot.
    """
    position_km: Tuple[float, float, float]
    velocity_km_s: Tuple[float, float, float]


def compare_states(
    computed: ReferenceState,
    reference: ReferenceState,
):
    """
    Compare two ECI states and compute absolute error vectors.

    Args:
        computed: State produced by Pyglspg4
        reference: Trusted reference state

    Returns:
        Tuple of:
            - position error vector (km)
            - velocity error vector (km/s)
    """

    pos_err = tuple(
        c - r for c, r in zip(computed.position_km, reference.position_km)
    )
    vel_err = tuple(
        c - r for c, r in zip(computed.velocity_km_s, reference.velocity_km_s)
    )

    return pos_err, vel_err

