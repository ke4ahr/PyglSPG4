# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
TLE validation utilities.
"""

from __future__ import annotations

from pyglspg4.api.exceptions import TLEError


def compute_checksum(line: str) -> int:
    """
    Compute the standard TLE checksum.
    """
    total = 0
    for ch in line[:-1]:
        if ch.isdigit():
            total += int(ch)
        elif ch == "-":
            total += 1
    return total % 10


def validate_tle_lines(line1: str, line2: str) -> None:
    if len(line1) < 69 or len(line2) < 69:
        raise TLEError("TLE lines must be at least 69 characters")

    if line1[0] != "1" or line2[0] != "2":
        raise TLEError("Invalid TLE line numbers")

    c1 = compute_checksum(line1)
    c2 = compute_checksum(line2)

    if int(line1[68]) != c1:
        raise TLEError("Checksum mismatch on line 1")

    if int(line2[68]) != c2:
        raise TLEError("Checksum mismatch on line 2")

