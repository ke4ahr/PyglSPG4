# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Ground-station pass prediction logic.
# Computes AOS, LOS, and max elevation passes.

import math
from pyglspg4.api.propagate import propagate
from pyglspg4.frames.teme_to_pef import teme_to_pef
from pyglspg4.frames.pef_to_itrf import pef_to_itrf
from pyglspg4.frames.itrf_to_geodetic import itrf_to_geodetic
from pyglspg4.time.julian import jd_from_datetime


def predict_passes(
    tle,
    station,
    start_dt,
    end_dt,
    step_sec=30.0,
    min_elevation_deg=0.0,
):
    """
    Predict satellite passes over a ground station.

    Parameters
    ----------
    tle : TLE
    station : GroundStation
    start_dt, end_dt : datetime
    step_sec : float
        Time step in seconds
    min_elevation_deg : float
        Minimum elevation for pass detection

    Returns
    -------
    list of dict
        Each dict contains AOS, LOS, max_el
    """

    passes = []
    in_pass = False
    current_pass = None

    tsince = 0.0
    tstep_min = step_sec / 60.0
    jd0 = jd_from_datetime(start_dt)

    t = start_dt
    while t <= end_dt:
        jd = jd_from_datetime(t)
        tsince = (jd - jd0) * 1440.0

        pos_teme, vel, err = propagate(tle, tsince)
        if err != 0:
            t += timedelta(seconds=step_sec)
            continue

        pos_pef = teme_to_pef(pos_teme, jd)
        pos_itrf = pef_to_itrf(pos_pef)

        rng, az, el = station.topocentric(pos_itrf)
        el_deg = math.degrees(el)

        if el_deg >= min_elevation_deg:
            if not in_pass:
                in_pass = True
                current_pass = {
                    "aos": t,
                    "max_el": el_deg,
                    "los": None,
                }
            else:
                current_pass["max_el"] = max(current_pass["max_el"], el_deg)
        else:
            if in_pass:
                current_pass["los"] = t
                passes.append(current_pass)
                in_pass = False
                current_pass = None

        t += timedelta(seconds=step_sec)

    return passes

