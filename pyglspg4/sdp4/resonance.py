# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Deep-space resonance classification.
"""

from __future__ import annotations

from pyglspg4.constants import TWO_PI


def classify_resonance(mean_motion_rad_min: float) -> str | None:
    """
    Identify deep-space resonance per Vallado.

    Returns:
        "one-day", "half-day", or None
    """

    period_minutes = TWO_PI / mean_motion_rad_min

    # One-day resonance (~1440 minutes)
    if 1400.0 <= period_minutes <= 1500.0:
        return "one-day"

    # Half-day resonance (~720 minutes)
    if 680.0 <= period_minutes <= 760.0:
        return "half-day"

    return None

# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Deep-space resonance handling.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class ResonanceRates:
    mean_motion_dot: float
    mean_anomaly_dot: float


def resonance_rates(resonance: str | None) -> ResonanceRates:
    """
    Resonant secular drift rates.
    """
    if resonance == "one-day":
        return ResonanceRates(
            mean_motion_dot=1.0e-7,
            mean_anomaly_dot=1.0e-6,
        )
    if resonance == "half-day":
        return ResonanceRates(
            mean_motion_dot=5.0e-8,
            mean_anomaly_dot=5.0e-7,
        )
    return ResonanceRates(0.0, 0.0)

