# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Deep-space propagation entry point.
"""

from __future__ import annotations

from pyglspg4.sdp4.state import SDP4State
from pyglspg4.sdp4.integrator import integrate_deep_space


def propagate_deep_space(
    state: SDP4State,
    tsince_minutes: float,
):
    """
    Perform deep-space propagation.

    NOTE:
    Orbital plane → ECI conversion occurs after Phase 4B.
    """
    return integrate_deep_space(state, tsince_minutes)

