# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Backend protocol for numerical operations.
"""

from __future__ import annotations

from typing import Protocol


class MathBackend(Protocol):
    sin: callable
    cos: callable
    sqrt: callable
    atan2: callable
    abs: callable

