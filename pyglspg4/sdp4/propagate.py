# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
SDP-4 deep-space propagator.

Coordinates deep-space propagation by combining secular integration,
periodic perturbation hooks, and final ECI frame construction.
This implementation is deterministic, thread-safe, and structured
to allow incremental completion of the full SDP-4 model.
"""

from __future__ import annotations

from pyglspg4.backend.base import MathBackend
from pyglspg4.sdp4.state import SDP4State
from pyglspg4.sdp4.integrator import IntegratorState, integrate_step
from pyglspg4.sdp4.periodic import apply_periodic_corrections
from pyglspg4.sdp4.eci import elements_to_eci


def propagate_deep_space(
    state: SDP4State,
    tsince_minutes: float,
    backend: MathBackend,
):
    """
    Propagate a deep-space orbit using a staged SDP-4 pipeline.

    Args:
        state: SDP4State
        tsince_minutes: Time since epoch (minutes)
        backend: MathBackend

    Returns:
        Tuple of:
            - position vector (km)
            - velocity vector (km/s)
    """

    # Initialize integrator state
    integ = IntegratorState(
        mean_anomaly=state.mean_anomaly,
        argument_of_perigee=state.argument_of_perigee,
        raan=state.raan,
    )

    # Secular integration (single-step placeholder)
    integ = integrate_step(integ, tsince_minutes)

    # Apply periodic corrections (currently no-op)
    mean_anomaly, argument_of_perigee, raan = apply_periodic_corrections(
        integ.mean_anomaly,
        integ.argument_of_perigee,
        integ.raan,
    )

    # Convert to ECI coordinates
    return elements_to_eci(
        mean_motion=state.mean_motion,
        eccentricity=state.eccentricity,
        inclination=state.inclination,
        argument_of_perigee=argument_of_perigee,
        raan=raan,
        mean_anomaly=mean_anomaly,
        backend=backend,
    )

