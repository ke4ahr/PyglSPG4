# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Parallel execution helpers.

Provides thin wrappers around concurrent.futures executors to enable
thread-safe and process-safe batch propagation while preserving
deterministic behavior.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Callable, Iterable, List, Any


def run_threaded(
    func: Callable[[Any], Any],
    tasks: Iterable[Any],
    max_workers: int | None = None,
) -> List[Any]:
    """
    Execute tasks in parallel using threads.

    Args:
        func: Callable applied to each task
        tasks: Iterable of task arguments
        max_workers: Optional maximum number of worker threads

    Returns:
        List of results in task order.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(func, tasks))
    return results


def run_processes(
    func: Callable[[Any], Any],
    tasks: Iterable[Any],
    max_workers: int | None = None,
) -> List[Any]:
    """
    Execute tasks in parallel using processes.

    Args:
        func: Callable applied to each task
        tasks: Iterable of task arguments
        max_workers: Optional maximum number of worker processes

    Returns:
        List of results in task order.

    Notes:
        Functions and arguments must be pickleable.
    """
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(func, tasks))
    return results

