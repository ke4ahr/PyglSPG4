# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Two-Line Element (TLE) validation utilities.

Provides basic structural and checksum validation for TLE line pairs
prior to parsing and propagation.
"""

from __future__ import annotations


class TLEValidationError(ValueError):
    """
    Raised when a TLE fails validation checks.
    """
    pass


def _checksum(line: str) -> int:
    """
    Compute the TLE checksum for a single line.

    The checksum is the sum of all digits plus one for each minus sign,
    modulo 10.
    """
    total = 0
    for char in line[:68]:
        if char.isdigit():
            total += int(char)
        elif char == "-":
            total += 1
    return total % 10


def validate_tle(line1: str, line2: str) -> None:
    """
    Validate a TLE line pair.

    Checks:
    - Line lengths
    - Line number identifiers
    - Checksums

    Raises:
        TLEValidationError if validation fails.
    """

    if len(line1) < 69 or len(line2) < 69:
        raise TLEValidationError("TLE lines must be at least 69 characters long")

    if not line1.startswith("1 ") or not line2.startswith("2 "):
        raise TLEValidationError("Invalid TLE line numbers")

    if _checksum(line1) != int(line1[68]):
        raise TLEValidationError("Checksum mismatch on line 1")

    if _checksum(line2) != int(line2[68]):
        raise TLEValidationError("Checksum mismatch on line 2")

