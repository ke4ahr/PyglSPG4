# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Batch propagation API.

Provides helpers for propagating multiple satellites sequentially
using a shared configuration and backend selection.
"""

from __future__ import annotations

from typing import Sequence

from pyglspg4.api.propagate import propagate


def propagate_batch(
    parsed_tles: Sequence,
    epochs: Sequence,
    backend: str | None = None,
):
    """
    Propagate multiple satellites sequentially.

    Args:
        parsed_tles: Sequence of ParsedTLE objects
        epochs: Sequence of Epoch objects
        backend: Optional backend selector ("numpy" or None)

    Returns:
        List of (position, velocity) tuples.
    """
    if len(parsed_tles) != len(epochs):
        raise ValueError("parsed_tles and epochs must be the same length")

    results = []
    for tle, epoch in zip(parsed_tles, epochs):
        results.append(propagate(tle, epoch, backend))

    return results

