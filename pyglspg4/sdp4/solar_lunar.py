# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Solar and lunar perturbation arguments.
"""

from __future__ import annotations
from dataclasses import dataclass

from pyglspg4.sdp4.constants import ZNS, ZNL


@dataclass(frozen=True)
class SolarLunarTerms:
    solar_mean_longitude: float
    lunar_mean_longitude: float


def compute_solar_lunar_terms(tsince_minutes: float) -> SolarLunarTerms:
    """
    Compute solar and lunar mean longitudes.

    Units: radians
    """
    solar = ZNS * tsince_minutes
    lunar = ZNL * tsince_minutes
    return SolarLunarTerms(
        solar_mean_longitude=solar,
        lunar_mean_longitude=lunar,
    )

