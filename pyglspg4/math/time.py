# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Time utilities for SGP-4 / SDP-4 propagation.

MINUTES_PER_DAY = 1440.0


def minutes_since_epoch(epoch_day, target_day):
    """
    Compute minutes since TLE epoch.

    Parameters
    ----------
    epoch_day : float
        Epoch day-of-year with fractional part
    target_day : float
        Target day-of-year with fractional part

    Returns
    -------
    float
        Minutes since epoch
    """
    return (target_day - epoch_day) * MINUTES_PER_DAY

