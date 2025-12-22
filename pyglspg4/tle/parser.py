# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Two-Line Element (TLE) parser.

Parses TLE line pairs into a structured, immutable representation
suitable for SGP-4 / SDP-4 initialization.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedTLE:
    """
    Immutable representation of a parsed TLE.
    """
    satellite_number: int
    epoch_year: int
    epoch_day: float
    inclination_deg: float
    raan_deg: float
    eccentricity: float
    argument_of_perigee_deg: float
    mean_anomaly_deg: float
    mean_motion_rev_per_day: float
    bstar: float


def parse_tle(line1: str, line2: str) -> ParsedTLE:
    """
    Parse a TLE line pair into a ParsedTLE object.

    This function assumes the input lines have already been validated
    for length and checksum.
    """

    satellite_number = int(line1[2:7])

    epoch_year = int(line1[18:20])
    epoch_day = float(line1[20:32])

    # BSTAR drag term (mantissa/exponent format)
    bstar_mantissa = float(line1[53:59]) * 1.0e-5
    bstar_exponent = int(line1[59:61])
    bstar = bstar_mantissa * (10.0 ** bstar_exponent)

    inclination = float(line2[8:16])
    raan = float(line2[17:25])
    eccentricity = float("0." + line2[26:33].strip())
    argument_of_perigee = float(line2[34:42])
    mean_anomaly = float(line2[43:51])
    mean_motion = float(line2[52:63])

    return ParsedTLE(
        satellite_number=satellite_number,
        epoch_year=epoch_year,
        epoch_day=epoch_day,
        inclination_deg=inclination,
        raan_deg=raan,
        eccentricity=eccentricity,
        argument_of_perigee_deg=argument_of_perigee,
        mean_anomaly_deg=mean_anomaly,
        mean_motion_rev_per_day=mean_motion,
        bstar=bstar,
    )

