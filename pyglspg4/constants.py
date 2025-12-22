# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.
#
# Pyglspg4 is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""
Physical and mathematical constants used by SGP-4.

Constants are read-only and must never be mutated.
"""

from __future__ import annotations

import math

# Mathematical constants
PI = math.pi
TWO_PI = 2.0 * math.pi

# Earth and gravitational constants (WGS-72)
# These values match the standard SGP-4 reference implementation.
EARTH_RADIUS_KM = 6378.135
MU_EARTH = 398600.8  # km^3 / s^2
KE = 0.0743669161
J2 = 1.082616e-3
J3 = -2.53881e-6
J4 = -1.65597e-6

# Time constants
SECONDS_PER_DAY = 86400.0
MINUTES_PER_DAY = 1440.0

# Numerical tolerances
KEPLER_EPSILON = 1e-12
MAX_KEPLER_ITERATIONS = 15

