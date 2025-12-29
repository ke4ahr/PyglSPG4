# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SDP-4 deep-space constants
# Source: NORAD Spacetrack Report #3
#         Vallado et al., AIAA 2006-6753

from __future__ import annotations

import math

# ---------------------------------------------------------------------------
# Fundamental constants
# ---------------------------------------------------------------------------

PI = math.pi
TWO_PI = 2.0 * PI

# ---------------------------------------------------------------------------
# Lunar–solar perturbation constants (per NORAD)
# ---------------------------------------------------------------------------

# Solar terms
ZES = 0.01675
ZNS = 1.19459e-5
C1SS = 2.9864797e-6
C1L = 4.7968065e-7
ZNL = 1.5835218e-4
ZEL = 0.05490

# Lunar terms
ZES_LUNAR = 0.01675
ZNS_LUNAR = 1.19459e-5
C1L_LUNAR = 4.7968065e-7
ZNL_LUNAR = 1.5835218e-4
ZEL_LUNAR = 0.05490

# ---------------------------------------------------------------------------
# Resonance coefficients
# ---------------------------------------------------------------------------

# Synchronous resonance (Earth rotation)
ROOT22 = 1.7891679e-6
ROOT32 = 3.7393792e-7
ROOT44 = 7.3636953e-9
ROOT52 = 1.1428639e-7
ROOT54 = 2.1765803e-9

# 12-hour resonance (Molniya)
THDT = 4.37526908801129966e-3

# ---------------------------------------------------------------------------
# Integration step parameters
# ---------------------------------------------------------------------------

# Step size for deep-space integrator [minutes]
DEEP_SPACE_STEP = 720.0

# Max number of integration steps
MAX_DEEP_STEPS = 10000

