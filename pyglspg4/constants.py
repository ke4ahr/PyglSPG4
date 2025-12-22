# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Fundamental physical and numerical constants for Pyglspg4.

Values are chosen to be consistent with standard SGP-4 / SDP-4
references (Vallado), and are treated as immutable.
"""

PI = 3.141592653589793
TWO_PI = 2.0 * PI

# Earth gravitational constant (SGP-4 units)
KE = 0.0743669161

# Earth equatorial radius (kilometers)
EARTH_RADIUS_KM = 6378.135

# Second zonal harmonic of the geopotential
J2 = 1.082616e-3

# Numerical parameters for Kepler solver
KEPLER_EPSILON = 1.0e-12
MAX_KEPLER_ITERATIONS = 20

# Time constants
SECONDS_PER_DAY = 86400.0

