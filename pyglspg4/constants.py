# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# NORAD / Vallado SGP-4 fundamental constants.
# Units follow Vallado convention (Earth radii, minutes, radians).

import math

# Mathematical constants
PI = math.pi
TWOPI = 2.0 * math.pi

# Earth and gravitational constants (WGS-72)
AE = 1.0                     # Earth radius (Earth radii)
XKE = 0.0743669161           # sqrt(GM) in Earth radii^1.5 / minute
CK2 = 5.413080e-4            # J2 harmonic
CK4 = 0.62098875e-6          # J4 harmonic
QOMS2T = 1.88027916e-9       # (Q0 - S)^4
S = 1.01222928               # Atmospheric drag parameter

# Earth rotation
OMEGA_E = 1.00273790934      # Earth rotation rate (rev/day)

# Derived constants
X2O3 = 2.0 / 3.0

# Time
MINUTES_PER_DAY = 1440.0
SECONDS_PER_DAY = 86400.0

# Error codes (NORAD compatible)
SGP4_SUCCESS = 0
SGP4_ERR_MEAN_ECCENTRICITY = 1
SGP4_ERR_MEAN_MOTION = 2
SGP4_ERR_DECAYED = 6

