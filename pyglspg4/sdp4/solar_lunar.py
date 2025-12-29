# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SDP-4 solar–lunar perturbation preprocessing
# Corresponds to NORAD dscom routine
# References:
#   - Spacetrack Report #3
#   - Vallado et al. (2006), Section 6

from __future__ import annotations

import math

from pyglspg4.constants import DEG2RAD
from pyglspg4.sdp4.constants import (
    ZES,
    ZNS,
    ZEL,
    ZNL,
    C1SS,
    C1L,
)
from pyglspg4.sdp4.state import SDP4State


def solar_lunar_precompute(state: SDP4State) -> None:
    """
    Precompute solar and lunar terms for deep-space propagation.

    This function initializes the deep-space secular and periodic
    coefficients used by SDP-4.
    """

    # Mean obliquity of the ecliptic (approx)
    eps = 23.43929111 * DEG2RAD

    sin_eps = math.sin(eps)
    cos_eps = math.cos(eps)

    # Solar terms
    state.sse = ZES * C1SS
    state.ssi = ZNS * C1SS * sin_eps
    state.ssl = ZNS * C1SS * cos_eps
    state.ssg = ZES * C1SS
    state.ssh = ZNS * C1SS
    state.ssd = ZNS * C1SS

    # Lunar terms (simplified; full theory applied in dpper)
    state.sse += ZEL * C1L
    state.ssi += ZNL * C1L * sin_eps
    state.ssl += ZNL * C1L * cos_eps
    state.ssg += ZEL * C1L
    state.ssh += ZNL * C1L
    state.ssd += ZNL * C1L

    # Mark as deep-space
    state.is_deep_space = True

