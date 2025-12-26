# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Example: Predict ISS passes over a fixed ground station.

from datetime import datetime, timedelta
import math

from pyglspg4.tle.parser import parse_tle
from pyglspg4.groundstation.station import GroundStation
from pyglspg4.groundstation.passes import predict_passes


ISS_TLE = (
    "1 25544U 98067A   24001.51869444  .00016717  00000-0  10270-3 0  9991",
    "2 25544  51.6405  24.4561 0004382  88.1684  38.3275 15.49745126398784",
)


def main():
    tle = parse_tle(*ISS_TLE)

    # Geographic center of Alabama (approximate)
    lat = math.radians(32.806671)
    lon = math.radians(-86.791130)
    alt_km = 0.2

    station = GroundStation(lat, lon, alt_km)

    start = datetime.utcnow()
    end = start + timedelta(days=2)

    passes = predict_passes(
        tle,
        station,
        start,
        end,
        step_sec=30.0,
        min_elevation_deg=10.0,
    )

    for p in passes:
        print(
            "AOS:", p["aos"],
            "LOS:", p["los"],
            "Max Elevation:", round(p["max_el"], 1), "deg"
        )


if __name__ == "__main__":
    main()

