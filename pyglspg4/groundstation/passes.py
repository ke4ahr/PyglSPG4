# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Ground station pass prediction
#
# Computes AOS, LOS, and maximum elevation events for
# satellites relative to a fixed ground station.
#
# Reference:
#   Vallado, Fundamentals of Astrodynamics and Applications

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional

from pyglspg4.sgp4.propagate import propagate
from pyglspg4.frames.itrf import teme_to_itrf
from pyglspg4.frames.geodetic import ecef_to_geodetic
from pyglspg4.groundstation.topocentric import topocentric
from pyglspg4.groundstation.visibility import is_visible


@dataclass(frozen=True)
class PassEvent:
    aos: float          # minutes since epoch
    los: float          # minutes since epoch
    max_el: float       # radians
    t_max: float        # minutes since epoch


def _sign(x: float) -> int:
    if x > 0.0:
        return 1
    if x < 0.0:
        return -1
    return 0


def predict_passes(
    state,
    lat: float,
    lon: float,
    alt: float,
    jd_start: float,
    minutes: float,
    step: float = 30.0,
    min_elevation: float = 0.0,
) -> List[PassEvent]:
    """
    Predict satellite passes over a ground station.

    Parameters
    ----------
    state : SGP4State
        Initialized SGP-4 / SDP-4 state
    lat : float
        Ground station latitude (rad)
    lon : float
        Ground station longitude (rad)
    alt : float
        Ground station altitude (km)
    jd_start : float
        Start Julian Date (UTC/UT1 aligned)
    minutes : float
        Duration to search forward (minutes)
    step : float
        Time step for coarse search (minutes)
    min_elevation : float
        Elevation mask (rad)

    Returns
    -------
    list of PassEvent
    """

    events: List[PassEvent] = []

    t = 0.0
    visible_prev = False
    aos: Optional[float] = None
    max_el = -math.pi / 2.0
    t_max = 0.0

    while t <= minutes:
        r_teme, v_teme, err = propagate(state, t)
        if err != 0:
            t += step
            continue

        jd = jd_start + t / 1440.0
        r_itrf, _ = teme_to_itrf(r_teme, v_teme, jd)

        az, el, _ = topocentric(r_itrf, lat, lon, alt)
        visible = is_visible(el, min_elevation)

        if visible and not visible_prev:
            aos = t
            max_el = el
            t_max = t

        if visible:
            if el > max_el:
                max_el = el
                t_max = t

        if not visible and visible_prev and aos is not None:
            events.append(
                PassEvent(
                    aos=aos,
                    los=t,
                    max_el=max_el,
                    t_max=t_max,
                )
            )
            aos = None
            max_el = -math.pi / 2.0

        visible_prev = visible
        t += step

    return events

