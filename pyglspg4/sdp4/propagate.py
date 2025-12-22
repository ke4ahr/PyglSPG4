# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

from __future__ import annotations

from pyglspg4.sdp4.integrator import integrate_deep_space
from pyglspg4.sdp4.periodic import apply_periodic_terms
from pyglspg4.sdp4.eci import deep_space_eci


def propagate_deep_space(
    state,
    tsince_minutes,
    backend,
):
    """
    Full deep-space SDP-4 propagation.
    """

    secular = integrate_deep_space(state, tsince_minutes)
    periodic = apply_periodic_terms(secular, tsince_minutes)

    return deep_space_eci(periodic, backend)

