# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Deep-space numerical integrator scaffolding for SDP-4.

Defines a deterministic, thread-safe integration framework for
advancing deep-space orbital elements over time. This module
intentionally provides a minimal structure suitable for extension
with full SDP-4 secular and periodic perturbation equations.
"""

from __future__ import annotations

from dataclasses import dataclass

from pyglspg4.sdp4.constants import EPSILON


@dataclass(frozen=True)
class IntegratorState:
    """
    Immutable integrator state snapshot.
    """
    mean_anomaly: float
    argument_of_perigee: float
    raan: float


def integrate_step(
    state: IntegratorState,
    delta_t: float,
):
    """
    Advance deep-space angular elements by a small time step.

    Args:
        state: Current IntegratorState
        delta_t: Time step (minutes)

    Returns:
        New IntegratorState advanced by delta_t.

    Notes:
        This function currently performs a linear phase advance and
        serves as a placeholder for the full SDP-4 integrator.
    """

    if abs(delta_t) < EPSILON:
        return state

    return IntegratorState(
        mean_anomaly=state.mean_anomaly + delta_t,
        argument_of_perigee=state.argument_of_perigee,
        raan=state.raan,
    )

