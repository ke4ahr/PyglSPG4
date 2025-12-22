# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Epoch handling utilities.

Defines an immutable Epoch abstraction built on Julian dates, used
throughout the propagation API to represent target times.
"""

from __future__ import annotations

from dataclasses import dataclass

from pyglspg4.time.julian import JulianDate


@dataclass(frozen=True)
class Epoch:
    """
    Immutable epoch representation.
    """
    jd: JulianDate

    @property
    def julian_date(self) -> float:
        """
        Return the Julian date as a floating-point value.
        """
        return self.jd.jd

