# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Deep-space secular integrator (SDP-4).
"""

from __future__ import annotations

from pyglspg4.sdp4.state import SDP4State
from pyglspg4.sdp4.solar_lunar import compute_solar_lunar_terms
from pyglspg4.sdp4.resonance import resonance_rates


def integrate_deep_space(
    state: SDP4State,
    tsince_minutes: float,
) -> SDP4State:
    """
    Apply deep-space secular perturbations.
    """

    terms = compute_solar_lunar_terms(tsince_minutes)
    rates = resonance_rates(state.resonance)

    # Secular updates
    new_mean_motion = (
        state.mean_motion + rates.mean_motion_dot * tsince_minutes
    )
    new_mean_anomaly = (
        state.mean_anomaly
        + rates.mean_anomaly_dot * tsince_minutes
        + terms.solar_mean_longitude
        + terms.lunar_mean_longitude
    )

    return SDP4State(
        mean_motion=new_mean_motion,
        eccentricity=state.eccentricity,
        inclination=state.inclination,
        argument_of_perigee=state.argument_of_perigee,
        raan=state.raan,
        mean_anomaly=new_mean_anomaly,
        resonance=state.resonance,
    )

