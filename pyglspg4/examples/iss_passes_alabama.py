# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Example: Predict ISS passes over Alabama (USA)

from datetime import datetime, timedelta, timezone

from pyglspg4.tle.parser import parse_tle_lines
from pyglspg4.api.propagate import propagate
from pyglspg4.groundstation.station import GroundStation
from pyglspg4.groundstation.pass_prediction import predict_passes

# ISS (ZARYA) – example TLE (replace with current)
tle_lines = [
    "1 25544U 98067A   25021.50000000  .00016717  00000+0  10270-3 0  9994",
    "2 25544  51.6412  89.1234 0004021 123.4567 234.5678 15.50312345678901",
]

tle = parse_tle_lines(tle_lines)

station = GroundStation(
    name="Alabama Center",
    latitude_deg=32.806671,
    longitude_deg=-86.791130,
    altitude_m=180.0,
)

start = datetime.now(timezone.utc)
end = start + timedelta(days=14)

passes = predict_passes(
    tle=tle,
    station=station,
    start_utc=start,
    end_utc=end,
    min_elevation_deg=10.0,
)

for p in passes:
    print(
        f"AOS: {p.aos_utc.isoformat()}  "
        f"LOS: {p.los_utc.isoformat()}  "
        f"MAX EL: {p.max_elevation_deg:.1f} deg"
    )

