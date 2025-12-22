# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
TLE parsing.
"""

from __future__ import annotations

from dataclasses import dataclass

from pyglspg4.api.exceptions import TLEError
from pyglspg4.tle.validator import validate_tle_lines


@dataclass(frozen=True)
class ParsedTLE:
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


def parse_tle(lines: list[str]) -> ParsedTLE:
    if len(lines) != 2:
        raise TLEError("TLE must contain exactly two lines")

    line1, line2 = lines
    validate_tle_lines(line1, line2)

    try:
        satnum = int(line1[2:7])
        epoch_year = int(line1[18:20])
        epoch_day = float(line1[20:32])

        bstar_raw = line1[53:61].strip()
        bstar = float(f"{bstar_raw[0:5]}e{bstar_raw[5:]}")

        inclination = float(line2[8:16])
        raan = float(line2[17:25])
        eccentricity = float(f"0.{line2[26:33].strip()}")
        argp = float(line2[34:42])
        mean_anomaly = float(line2[43:51])
        mean_motion = float(line2[52:63])

    except Exception as exc:
        raise TLEError("Failed to parse TLE fields") from exc

    return ParsedTLE(
        satellite_number=satnum,
        epoch_year=epoch_year,
        epoch_day=epoch_day,
        inclination_deg=inclination,
        raan_deg=raan,
        eccentricity=eccentricity,
        argument_of_perigee_deg=argp,
        mean_anomaly_deg=mean_anomaly,
        mean_motion_rev_per_day=mean_motion,
        bstar=bstar,
    )

