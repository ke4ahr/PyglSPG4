# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Ground-station pass prediction engine
#
# Computes satellite rise, culmination, and set events
# over a specified time window using SGP-4 / SDP-4
# propagation and Earth-fixed geometry.
#
# References:
#   Vallado, Fundamentals of Astrodynamics and Applications

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Callable, List, Tuple

from pyglspg4.frames.teme_to_itrf import teme_to_itrf
from pyglspg4.ground.enu import ecef_to_enu
from pyglspg4.ground.geodetic import ecef_to_geodetic
from pyglspg4.ground.visibility import az_el_range
from pyglspg4.time.julian import datetime_to_jd


@dataclass
class PassEvent:
    aos: datetime.datetime
    los: datetime.datetime
    tca: datetime.datetime
    max_elevation_rad: float


def predict_passes(
    propagate_fn: Callable[[float], Tuple[Tuple[float, float, float], Tuple[float, float, float]]],
    eop,
    site_ecef: Tuple[float, float, float],
    site_lat_rad: float,
    site_lon_rad: float,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    step_seconds: int = 30,
    min_elevation_rad: float = 0.0,
) -> List[PassEvent]:
    """
    Predict satellite passes over a ground station.

    Parameters
    ----------
    propagate_fn : callable
        Function returning TEME position & velocity given tsince_minutes
    eop : EOPTable
        Earth Orientation Parameters
    site_ecef : (x, y, z)
        Ground station ECEF position (km)
    site_lat_rad : float
        Ground station latitude (radians)
    site_lon_rad : float
        Ground station longitude (radians)
    start_time, end_time : datetime
        Search window (UTC)
    step_seconds : int
        Time step (seconds)
    min_elevation_rad : float
        Elevation mask (radians)

    Returns
    -------
    passes : list of PassEvent
    """

    passes: List[PassEvent] = []

    in_pass = False
    aos = los = tca = None
    max_el = -1.0

    t = start_time
    while t <= end_time:
        jd = datetime_to_jd(t)
        tsince_min = (jd - datetime_to_jd(start_time)) * 1440.0

        r_teme, v_teme = propagate_fn(tsince_min)
        r_ecef, _ = teme_to_itrf(r_teme, v_teme, jd, eop)

        e, n, u = ecef_to_enu(r_ecef, site_ecef, site_lat_rad, site_lon_rad)
        az, el, _ = az_el_range(e, n, u)

        if el >= min_elevation_rad:
            if not in_pass:
                in_pass = True
                aos = t
                max_el = el
                tca = t
            else:
                if el > max_el:
                    max_el = el
                    tca = t
        else:
            if in_pass:
                los = t
                passes.append(
                    PassEvent(
                        aos=aos,
                        los=los,
                        tca=tca,
                        max_elevation_rad=max_el,
                    )
                )
                in_pass = False

        t += datetime.timedelta(seconds=step_seconds)

    return passes

