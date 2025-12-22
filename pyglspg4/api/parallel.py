# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Parallel propagation API.

Provides helpers for propagating multiple satellites in parallel
using thread-based or process-based execution, while preserving
deterministic behavior and thread safety.
"""

from __future__ import annotations

from typing import Sequence

from pyglspg4.api.propagate import propagate
from pyglspg4.parallel.executors import run_threaded, run_processes


def propagate_parallel(
    parsed_tles: Sequence,
    epochs: Sequence,
    backend: str | None = None,
    mode: str = "thread",
    max_workers: int | None = None,
):
    """
    Propagate multiple satellites in parallel.

    Args:
        parsed_tles: Sequence of ParsedTLE objects
        epochs: Sequence of Epoch objects
        backend: Optional backend selector ("numpy" or None)
        mode: Execution mode, one of:
              - "thread"  (ThreadPoolExecutor, default)
              - "process" (ProcessPoolExecutor)
        max_workers: Optional maximum number of worker threads/processes

    Returns:
        List of (position, velocity) tuples.
    """

    if len(parsed_tles) != len(epochs):
        raise ValueError("parsed_tles and epochs must be the same length")

    tasks = list(zip(parsed_tles, epochs))

    def _task(args):
        tle, epoch = args
        return propagate(tle, epoch, backend)

    if mode == "thread":
        return run_threaded(_task, tasks, max_workers)

    if mode == "process":
        return run_processes(_task, tasks, max_workers)

    raise ValueError(f"Unknown parallel execution mode: {mode}")

