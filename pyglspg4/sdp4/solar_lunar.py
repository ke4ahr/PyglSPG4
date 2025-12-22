# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Solar and lunar perturbation scaffolding for SDP-4.

This module defines placeholder structures and deterministic hooks
for incorporating solar and lunar gravitational perturbations into
the deep-space (SDP-4) propagation path.

Full analytical perturbation models (per Vallado / Hoots & Roehrich)
are intentionally staged for incremental implementation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SolarLunarTerms:
    """
    Container for precomputed solar and lunar perturbation terms.

    All values are dimensionless or normalized per SDP-4 conventions.
    """
    solar_term: float = 0.0
    lunar_term: float = 0.0


def compute_solar_lunar_terms(
    mean_motion: float,
    eccentricity: float,
    inclination: float,
):
    """
    Compute solar and lunar perturbation terms.

    Args:
        mean_motion: Mean motion (rad/min)
        eccentricity: Orbital eccentricity
        inclination: Orbital inclination (rad)

    Returns:
        SolarLunarTerms instance.

    Notes:
        This function currently returns zeroed terms and serves
        as a stable API placeholder for future deep-space modeling.
    """
    return SolarLunarTerms()

