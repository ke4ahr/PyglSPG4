# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Batch propagation API.
"""

from __future__ import annotations

from typing import Iterable, Sequence

from pyglspg4.api.propagate import propagate


def propagate_batch(
    parsed_tles: Sequence,
    epochs: Sequence,
    backend: str | None = None,
):
    """
    Propagate multiple satellites sequentially.

    Deterministic reference implementation.
    """
    if len(parsed_tles) != len(epochs):
        raise ValueError("parsed_tles and epochs must be same length")

    results = []
    for tle, epoch in zip(parsed_tles, epochs):
        results.append(propagate(tle, epoch, backend))
    return results

