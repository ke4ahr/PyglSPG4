# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Minimal vector math utilities for orbital mechanics.
# Explicit implementation, no NumPy dependency.

import math


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm(v):
    return math.sqrt(dot(v, v))


def scale(v, s):
    return (v[0] * s, v[1] * s, v[2] * s)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

