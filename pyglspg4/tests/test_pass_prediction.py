# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Integration tests for ground-station pass prediction.

from datetime import datetime, timedelta
import math

from pyglspg4.tle.parser import parse_tle
from pyglspg4.groundstation.station import GroundStation
from pyglspg4.groundstation.passes import predict_passes


ISS_TLE = (
    "1 25544U 98067A   24001.51869444  .00016717  00000-0  10270-3 0  9991",
    "2 25544  51.6405  24.4561 0004382  88.1684  38.3275 15.49745126398784",
)


def test_pass_prediction_runs():
    tle = parse_tle(*ISS_TLE)

    # Geographic center of Alabama (approx)
    lat = math.radians(32.806671)
    lon = math.radians(-86.791130)
    alt = 0.2  # km

    station = GroundStation(lat, lon, alt)

    start = datetime(2025, 1, 1, 0, 0, 0)
    end = start + timedelta(days=1)

    passes = predict_passes(
        tle,
        station,
        start,
        end,
        step_sec=60.0,
        min_elevation_deg=10.0,
    )

    assert isinstance(passes, list)
    for p in passes:
        assert "aos" in p
        assert "los" in p
        assert "max_el" in p
        assert p["max_el"] >= 10.0

