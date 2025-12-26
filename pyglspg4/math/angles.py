# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Angle normalization utilities for SGP-4 / SDP-4.
# Deterministic, thread-safe, no external dependencies.

import math

TWOPI = 2.0 * math.pi


def wrap_two_pi(angle):
    """
    Normalize angle to the range [0, 2π).
    """
    return angle % TWOPI


def wrap_pi(angle):
    """
    Normalize angle to the range (-π, π].
    """
    a = angle % TWOPI
    if a > math.pi:
        a -= TWOPI
    return a

