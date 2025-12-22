# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
NumPy-oriented vector propagation helpers.
"""

from __future__ import annotations

import numpy as np

from pyglspg4.api.batch import propagate_batch


def propagate_numpy(
    parsed_tles,
    epochs,
):
    """
    NumPy-friendly wrapper.

    Returns arrays of positions and velocities.
    """
    results = propagate_batch(parsed_tles, epochs, backend="numpy")

    positions = np.array([r[0] for r in results])
    velocities = np.array([r[1] for r in results])

    return positions, velocities

