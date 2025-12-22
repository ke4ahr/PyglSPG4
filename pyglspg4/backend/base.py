# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Backend protocol for numerical operations.

Defines the minimal math interface required by Pyglspg4 so that
pure-Python and NumPy backends can be used interchangeably.
"""

from __future__ import annotations

from typing import Protocol, Callable


class MathBackend(Protocol):
    sin: Callable[[float], float]
    cos: Callable[[float], float]
    sqrt: Callable[[float], float]
    atan2: Callable[[float, float], float]
    abs: Callable[[float], float]

