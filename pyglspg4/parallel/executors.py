# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Parallel execution backends.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Callable, Iterable


def run_threaded(
    fn: Callable,
    args: Iterable,
    max_workers: int | None = None,
):
    """
    Thread-based execution (safe default).
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(fn, args))


def run_processes(
    fn: Callable,
    args: Iterable,
    max_workers: int | None = None,
):
    """
    Process-based execution.

    Caller is responsible for ensuring picklability.
    """
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(fn, args))

