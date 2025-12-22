# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Pure Python math backend.
"""

import math


class PythonBackend:
    sin = staticmethod(math.sin)
    cos = staticmethod(math.cos)
    sqrt = staticmethod(math.sqrt)
    atan2 = staticmethod(math.atan2)
    abs = staticmethod(abs)

