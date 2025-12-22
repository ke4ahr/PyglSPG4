# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Julian date utilities.

Provides conversion between calendar dates and Julian dates,
used internally for epoch handling and time propagation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JulianDate:
    """
    Immutable Julian Date representation.
    """
    jd: float


def calendar_to_julian(
    year: int,
    month: int,
    day: int,
    hour: int = 0,
    minute: int = 0,
    second: float = 0.0,
) -> JulianDate:
    """
    Convert a calendar date to a Julian Date.

    Algorithm valid for Gregorian calendar dates.
    """

    if month <= 2:
        year -= 1
        month += 12

    a = year // 100
    b = 2 - a + (a // 4)

    day_fraction = (
        hour / 24.0
        + minute / 1440.0
        + second / 86400.0
    )

    jd = (
        int(365.25 * (year + 4716))
        + int(30.6001 * (month + 1))
        + day
        + day_fraction
        + b
        - 1524.5
    )

    return JulianDate(jd)

