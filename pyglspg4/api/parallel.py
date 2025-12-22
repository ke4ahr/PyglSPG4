# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Parallel propagation API.
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
    Parallel propagation of satellites.

    mode:
        "thread"  - ThreadPoolExecutor (default)
        "process" - ProcessPoolExecutor
    """

    if len(parsed_tles) != len(epochs):
        raise ValueError("parsed_tles and epochs must be same length")

    tasks = list(zip(parsed_tles, epochs))

    def task(arg):
        tle, epoch = arg
        return propagate(tle, epoch, backend)

    if mode == "thread":
        return run_threaded(task, tasks, max_workers)
    if mode == "process":
        return run_processes(task, tasks, max_workers)

    raise ValueError(f"Unknown mode: {mode}")

