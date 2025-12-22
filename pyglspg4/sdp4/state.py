# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
SDP-4 deep-space state representation.

Defines the immutable state parameters required for SDP-4 propagation,
including resonance classification.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SDP4State:
    """
    Immutable SDP-4 state.
    """
    mean_motion: float
    eccentricity: float
    inclination: float
    argument_of_perigee: float
    raan: float
    mean_anomaly: float
    resonance: int

