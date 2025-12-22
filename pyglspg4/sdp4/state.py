# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Deep-space (SDP-4) internal state.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class SDP4State:
    mean_motion: float
    eccentricity: float
    inclination: float
    argument_of_perigee: float
    raan: float
    mean_anomaly: float
    resonance: str | None

