i# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Script: Print a human-readable satellite pass table.

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

    # Geographic center of Alabama
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

    if not passes:
        print("No passes found.")
        return

    print("Satellite Passes")
    print("-" * 60)
    for p in passes:
        print(
            "AOS:",
            p["aos"].strftime("%Y-%m-%d %H:%M:%S"),
            "LOS:",
            p["los"].strftime("%Y-%m-%d %H:%M:%S"),
            "Max El:",
            f"{p['max_el']:.1f} deg",
        )


if __name__ == "__main__":
    main()

