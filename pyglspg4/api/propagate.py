# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Unified propagation API.
# Dispatches to SGP-4 (near-Earth) or SDP-4 (deep-space).

from pyglspg4.tle.validator import validate_tle
from pyglspg4.sgp4.initializer import initialize_sgp4
from pyglspg4.sgp4.near_earth import propagate_near_earth


def propagate(tle, tsince_min):
    """
    Propagate satellite state from TLE.

    Parameters
    ----------
    tle : TLE
        Parsed TLE object
    tsince_min : float
        Minutes since epoch

    Returns
    -------
    (pos_km, vel_km_s, error_code)
    """

    validate_tle(tle)

    # NOTE: Deep-space detection hook reserved for SDP-4
    state = initialize_sgp4(tle)

    return propagate_near_earth(state, tsince_min)

