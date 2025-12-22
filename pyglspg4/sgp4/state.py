# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
SGP-4 near-Earth state representation.

Defines the immutable state parameters required for SGP-4 propagation
after TLE initialization.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SGP4State:
    """
    Immutable SGP-4 state.
    """
    mean_motion: float
    eccentricity: float
    inclination: float
    argument_of_perigee: float
    raan: float
    mean_anomaly: float

