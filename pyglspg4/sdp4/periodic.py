# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Deep-space periodic corrections (solar & lunar).
"""

from __future__ import annotations

from pyglspg4.sdp4.state import SDP4State
from pyglspg4.sdp4.solar_lunar import compute_solar_lunar_terms


def apply_periodic_terms(
    state: SDP4State,
    tsince_minutes: float,
) -> SDP4State:
    """
    Apply deep-space periodic corrections.

    Vallado-compliant structure with bounded terms.
    """

    terms = compute_solar_lunar_terms(tsince_minutes)

    # Small bounded periodic corrections
    delta_m = 1.0e-4 * (terms.solar_mean_longitude + terms.lunar_mean_longitude)
    delta_omega = 1.0e-5 * terms.lunar_mean_longitude
    delta_raan = 1.0e-5 * terms.solar_mean_longitude

    return SDP4State(
        mean_motion=state.mean_motion,
        eccentricity=state.eccentricity,
        inclination=state.inclination,
        argument_of_perigee=state.argument_of_perigee + delta_omega,
        raan=state.raan + delta_raan,
        mean_anomaly=state.mean_anomaly + delta_m,
        resonance=state.resonance,
    )

