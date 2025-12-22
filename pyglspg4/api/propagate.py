# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Public propagation API.
"""

from __future__ import annotations

from pyglspg4.backend.selector import select_backend
from pyglspg4.sgpsg4.near_earth import propagate_near_earth
from pyglspg4.sgpsg4.initializer import initialize_sgp4
from pyglspg4.time.epochs import Epoch
from pyglspg4.api.exceptions import PropagationError
from pyglspg4.sdp4.state import SDP4State
from pyglspg4.sdp4.resonance import classify_resonance
from pyglspg4.sdp4.propagate import propagate_deep_space


def propagate(parsed_tle, epoch: Epoch, backend: str | None = None):
    """
    Propagate a satellite to the given epoch.

    Returns position and velocity in ECI frame.
    """

    be = select_backend(backend)
    init = initialize_sgp4(parsed_tle)

    if init.is_deep_space:
        raise PropagationError("Deep-space orbits not yet implemented")

    # Time since epoch in minutes
    tsince_days = epoch.jd.jd - parsed_tle.epoch_day
    tsince_minutes = tsince_days * 1440.0

    return propagate_near_earth(
        init.state,
        tsince_minutes,
        be,
    )

