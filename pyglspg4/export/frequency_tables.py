# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Automatic pass-time frequency tables
#
# Generates Doppler-corrected frequency tables for
# satellite passes suitable for CAT control, APRS,
# and planning purposes.
#
# Reference:
#   Vallado, Fundamentals of Astrodynamics and Applications

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, asdict
from typing import List, Tuple

from pyglspg4.sgp4.propagate import propagate
from pyglspg4.frames.itrf import teme_to_itrf
from pyglspg4.groundstation.doppler import doppler_shift
from pyglspg4.groundstation.topocentric import topocentric


@dataclass(frozen=True)
class FrequencyPoint:
    time_min: float
    azimuth_rad: float
    elevation_rad: float
    frequency_hz: float


def generate_frequency_table(
    state,
    lat: float,
    lon: float,
    alt: float,
    jd_start: float,
    aos: float,
    los: float,
    base_frequency_hz: float,
    step: float = 10.0,
) -> List[FrequencyPoint]:
    """
    Generate Doppler-corrected frequency table for a pass.

    Parameters
    ----------
    state : SGP4State
        Initialized propagator state
    lat, lon, alt : float
        Ground station geodetic coordinates (rad, rad, km)
    jd_start : float
        Julian Date at t=0
    aos : float
        Acquisition of signal time (minutes since epoch)
    los : float
        Loss of signal time (minutes since epoch)
    base_frequency_hz : float
        Nominal transmit frequency
    step : float
        Time step (minutes)

    Returns
    -------
    list of FrequencyPoint
    """

    points: List[FrequencyPoint] = []

    t = aos
    while t <= los:
        r_teme, v_teme, err = propagate(state, t)
        if err != 0:
            t += step
            continue

        jd = jd_start + t / 1440.0
        r_itrf, v_itrf = teme_to_itrf(r_teme, v_teme, jd)

        az, el, rho = topocentric(r_itrf, lat, lon, alt)

        # Ground station velocity is negligible for most use cases
        v_site = (0.0, 0.0, 0.0)
        r_site = (0.0, 0.0, 0.0)

        freq = doppler_shift(
            r_itrf,
            v_itrf,
            r_site,
            v_site,
            base_frequency_hz,
        )

        points.append(
            FrequencyPoint(
                time_min=t,
                azimuth_rad=az,
                elevation_rad=el,
                frequency_hz=freq,
            )
        )

        t += step

    return points


def export_frequency_table_csv(
    table: List[FrequencyPoint],
    path: str,
) -> None:
    """
    Export frequency table to CSV.

    Parameters
    ----------
    table : list of FrequencyPoint
    path : str
        Output file path
    """

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["time_min", "azimuth_rad", "elevation_rad", "frequency_hz"]
        )
        for p in table:
            writer.writerow(
                [
                    p.time_min,
                    p.azimuth_rad,
                    p.elevation_rad,
                    p.frequency_hz,
                ]
            )


def export_frequency_table_json(
    table: List[FrequencyPoint],
    path: str,
) -> None:
    """
    Export frequency table to JSON.

    Parameters
    ----------
    table : list of FrequencyPoint
    path : str
        Output file path
    """

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            [asdict(p) for p in table],
            f,
            indent=2,
        )

