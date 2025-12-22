# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Unified propagation API.

Provides a single entry point for propagating satellites using
SGP-4 (near-Earth) or SDP-4 (deep-space) models, selected
automatically based on orbital period.
"""

from __future__ import annotations

from pyglspg4.backend.selector import select_backend
from pyglspg4.sgpsg4.initializer import initialize_sgp4
from pyglspg4.sgpsg4.near_earth import propagate_near_earth
from pyglspg4.sdp4.state import SDP4State
from pyglspg4.sdp4.resonance import classify_resonance
from pyglspg4.sdp4.propagate import propagate_deep_space


def propagate(parsed_tle, epoch, backend: str | None = None):
    """
    Propagate a satellite to a given epoch.

    Args:
        parsed_tle: ParsedTLE instance
        epoch: Epoch instance
        backend: Optional backend selector ("numpy" or None)

    Returns:
        Tuple of:
            - position vector (km)
            - velocity vector (km/s)
    """

    be = select_backend(backend)
    init = initialize_sgp4(parsed_tle)

    # Time since epoch in minutes
    tsince_minutes = (epoch.jd.jd - parsed_tle.epoch_day) * 1440.0

    # Near-Earth propagation
    if not init.is_deep_space:
        pv = propagate_near_earth(init.state, tsince_minutes, be)
        return pv.position_km, pv.velocity_km_s

    # Deep-space propagation
    resonance = classify_resonance(init.mean_motion_rad_per_min)

    deep_state = SDP4State(
        mean_motion=init.state.mean_motion,
        eccentricity=init.state.eccentricity,
        inclination=init.state.inclination,
        argument_of_perigee=init.state.argument_of_perigee,
        raan=init.state.raan,
        mean_anomaly=init.state.mean_anomaly,
        resonance=resonance,
    )

    return propagate_deep_space(deep_state, tsince_minutes, be)

