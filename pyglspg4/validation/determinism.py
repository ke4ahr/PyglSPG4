# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Determinism verification utilities.
"""

from __future__ import annotations


def assert_deterministic(fn, args, runs: int = 5):
    """
    Ensure repeated executions produce identical results.
    """
    first = fn(*args)
    for _ in range(runs - 1):
        if fn(*args) != first:
            raise AssertionError("Non-deterministic behavior detected")

