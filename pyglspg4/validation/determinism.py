# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Determinism validation utilities.

Provides helpers to verify that Pyglspg4 propagation results are
bitwise-consistent across repeated runs, threads, and execution modes.
"""

from __future__ import annotations

from typing import Callable, Any, Tuple


def assert_deterministic(
    func: Callable[[], Tuple[Any, Any]],
    repeats: int = 5,
):
    """
    Assert that a callable returns identical results across runs.

    Args:
        func: Zero-argument callable returning a result tuple
        repeats: Number of times to repeat execution

    Raises:
        AssertionError if results differ across runs.
    """

    first = func()
    for _ in range(repeats - 1):
        if func() != first:
            raise AssertionError("Non-deterministic behavior detected")

