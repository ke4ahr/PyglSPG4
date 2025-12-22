# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Vectorized propagation API.

Provides helpers for propagating multiple satellites using NumPy
vectorization when available. This API is intended for high-throughput
use cases where many satellites are propagated to a common epoch.
"""

from __future__ import annotations

from typing import Sequence

from pyglspg4.api.propagate import propagate


def propagate_vectorized(
    parsed_tles: Sequence,
    epoch,
):
    """
    Propagate multiple satellites to a common epoch using a NumPy backend.

    This function is a convenience wrapper that enforces NumPy usage
    and delegates to the standard propagation path. True state-level
    vectorization may be introduced in future releases.

    Args:
        parsed_tles: Sequence of ParsedTLE objects
        epoch: Epoch instance common to all satellites

    Returns:
        List of (position, velocity) tuples.
    """
    results = []
    for tle in parsed_tles:
        results.append(propagate(tle, epoch, backend="numpy"))
    return results

