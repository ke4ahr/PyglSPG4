# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Julian date utilities.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from pyglspg4.constants import SECONDS_PER_DAY


@dataclass(frozen=True)
class JulianDate:
    """
    Immutable Julian Date representation.
    """
    jd: float

    @classmethod
    def from_datetime(cls, dt: datetime) -> "JulianDate":
        if dt.tzinfo is None:
            raise ValueError("Datetime must be timezone-aware")

        dt = dt.astimezone(timezone.utc)

        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour
        minute = dt.minute
        second = dt.second + dt.microsecond / 1e6

        if month <= 2:
            year -= 1
            month += 12

        a = year // 100
        b = 2 - a + a // 4

        jd_day = int(365.25 * (year + 4716))
        jd_month = int(30.6001 * (month + 1))

        jd = (
            jd_day
            + jd_month
            + day
            + b
            - 1524.5
        )

        frac = (hour * 3600.0 + minute * 60.0 + second) / SECONDS_PER_DAY

        return cls(jd + frac)

