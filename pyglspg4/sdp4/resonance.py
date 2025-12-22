# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Deep-space resonance classification.

Determines whether a satellite orbit falls into a deep-space resonance
category relevant to SDP-4 propagation.
"""

from __future__ import annotations

from pyglspg4.sdp4.constants import (
    RESONANCE_NONE,
    RESONANCE_HALF_DAY,
    RESONANCE_ONE_DAY,
)


def classify_resonance(mean_motion_rad_per_min: float) -> int:
    """
    Classify orbital resonance based on mean motion.

    Args:
        mean_motion_rad_per_min: Mean motion in radians per minute

    Returns:
        One of the RESONANCE_* constants.
    """

    # Convert mean motion to orbital period in minutes
    period_minutes = (2.0 * 3.141592653589793) / mean_motion_rad_per_min

    # Approximate resonance bands
    if 680.0 <= period_minutes <= 760.0:
        return RESONANCE_ONE_DAY

    if 340.0 <= period_minutes <= 390.0:
        return RESONANCE_HALF_DAY

    return RESONANCE_NONE

