# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
NumPy-accelerated math backend.

Implements the MathBackend protocol using NumPy vectorized functions.
This backend enables batch and parallel propagation with improved
performance when NumPy is available.
"""

import numpy as np


class NumPyBackend:
    sin = staticmethod(np.sin)
    cos = staticmethod(np.cos)
    sqrt = staticmethod(np.sqrt)
    atan2 = staticmethod(np.arctan2)
    abs = staticmethod(np.abs)

