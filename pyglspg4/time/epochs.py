# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Epoch handling and normalization.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from pyglspg4.time.julian import JulianDate


@dataclass(frozen=True)
class Epoch:
    """
    Immutable epoch wrapper.
    """
    jd: JulianDate

    @classmethod
    def from_datetime(cls, dt: datetime) -> "Epoch":
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return cls(JulianDate.from_datetime(dt))

    @classmethod
    def from_iso8601(cls, value: str) -> "Epoch":
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return cls.from_datetime(dt)

