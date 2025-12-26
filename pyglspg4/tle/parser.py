# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Two-Line Element (TLE) parser.
# Strict, deterministic parsing consistent with NORAD format.

from dataclasses import dataclass


@dataclass(frozen=True)
class TLE:
    satnum: int
    classification: str
    int_desig: str
    epoch_year: int
    epoch_day: float
    mean_motion_dot: float
    mean_motion_ddot: float
    bstar: float
    inclination: float
    raan: float
    eccentricity: float
    arg_perigee: float
    mean_anomaly: float
    mean_motion: float
    rev_number: int


def _parse_exponential(field):
    """
    Parse TLE exponential notation (e.g., 20323-4).
    """
    if not field.strip():
        return 0.0
    base = float(field[:-2]) * 1e-5
    exp = int(field[-2:])
    return base * (10.0 ** exp)


def parse_tle(line1, line2):
    """
    Parse TLE line pair into TLE dataclass.
    """

    if len(line1) < 69 or len(line2) < 69:
        raise ValueError("Invalid TLE line length")

    satnum = int(line1[2:7])
    classification = line1[7]
    int_desig = line1[9:17].strip()

    epoch_year = int(line1[18:20])
    epoch_year += 2000 if epoch_year < 57 else 1900
    epoch_day = float(line1[20:32])

    mean_motion_dot = float(line1[33:43])
    mean_motion_ddot = _parse_exponential(line1[44:52])
    bstar = _parse_exponential(line1[53:61])

    inclination = float(line2[8:16])
    raan = float(line2[17:25])
    eccentricity = float("0." + line2[26:33])
    arg_perigee = float(line2[34:42])
    mean_anomaly = float(line2[43:51])
    mean_motion = float(line2[52:63])
    rev_number = int(line2[63:68])

    return TLE(
        satnum=satnum,
        classification=classification,
        int_desig=int_desig,
        epoch_year=epoch_year,
        epoch_day=epoch_day,
        mean_motion_dot=mean_motion_dot,
        mean_motion_ddot=mean_motion_ddot,
        bstar=bstar,
        inclination=inclination,
        raan=raan,
        eccentricity=eccentricity,
        arg_perigee=arg_perigee,
        mean_anomaly=mean_anomaly,
        mean_motion=mean_motion,
        rev_number=rev_number,
    )

