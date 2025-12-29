# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# NORAD SGP-4 / SDP-4 fundamental constants
# Source: Vallado et al., "Revisiting Spacetrack Report #3", AIAA 2006-6753

from __future__ import annotations

import math

# ---------------------------------------------------------------------------
# Mathematical constants
# ---------------------------------------------------------------------------

PI = math.pi
TWO_PI = 2.0 * math.pi
DEG2RAD = PI / 180.0
RAD2DEG = 180.0 / PI

# ---------------------------------------------------------------------------
# Earth and gravity model (WGS-72 per NORAD SGP-4)
# ---------------------------------------------------------------------------

# Earth equatorial radius [km]
AE = 1.0

# Earth radius in km used by SGP-4
EARTH_RADIUS_KM = 6378.135

# Gravitational parameter (mu) [km^3 / s^2]
MU = 398600.8

# Minutes per day
MINUTES_PER_DAY = 1440.0

# Seconds per minute
SECONDS_PER_MINUTE = 60.0

# ---------------------------------------------------------------------------
# SGP-4 specific constants
# ---------------------------------------------------------------------------

# Reciprocal of tumin (minutes in one TU)
XKE = 60.0 / math.sqrt(
    (EARTH_RADIUS_KM ** 3) / MU
)

# Second zonal harmonic
CK2 = 5.413080e-4

# Fourth zonal harmonic
CK4 = 0.62098875e-6

# QOMS2T = (Q0 - S)^4
# Q0 = 120 km, S = 78 km
QOMS2T = ((120.0 - 78.0) / EARTH_RADIUS_KM) ** 4

# S atmospheric parameter
S = 78.0 / EARTH_RADIUS_KM + 1.0

# ---------------------------------------------------------------------------
# Derived constants
# ---------------------------------------------------------------------------

# Earth rotation rate [rad/min]
OMEGA_EARTH = 7.29211514670698e-5 * 60.0

# Keplerian constants
X2O3 = 2.0 / 3.0

# ---------------------------------------------------------------------------
# Error codes (per NORAD)
# ---------------------------------------------------------------------------

SGP4_ERROR_NONE = 0
SGP4_ERROR_ECCENTRICITY = 1
SGP4_ERROR_MEAN_MOTION = 2
SGP4_ERROR_ORBITAL_DECAY = 3
SGP4_ERROR_SUBORBITAL = 4
SGP4_ERROR_DEEP_SPACE = 5

# ---------------------------------------------------------------------------
# Utility validation helpers
# ---------------------------------------------------------------------------

def validate_eccentricity(ecc: float) -> None:
    if ecc < 0.0 or ecc >= 1.0:
        raise ValueError(f"Invalid eccentricity: {ecc}")

def validate_mean_motion(n0: float) -> None:
    if n0 <= 0.0:
        raise ValueError(f"Invalid mean motion: {n0}")

def is_deep_space(mean_motion_rev_per_day: float) -> bool:
    """
    Deep-space if orbital period >= 225 minutes.
    """
    period_minutes = MINUTES_PER_DAY / mean_motion_rev_per_day
    return period_minutes >= 225.0

