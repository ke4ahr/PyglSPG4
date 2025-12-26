# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Example: Define a ground station at the geographic center of Alabama
# and print its ECEF coordinates.

import math
from pyglspg4.groundstation.station import GroundStation


def main():
    # Approximate geographic center of Alabama
    lat_deg = 32.806671
    lon_deg = -86.791130
    alt_km = 0.2

    lat = math.radians(lat_deg)
    lon = math.radians(lon_deg)

    station = GroundStation(lat, lon, alt_km)

    ecef = station.ecef_position()

    print("Ground Station (Alabama)")
    print("Latitude (deg):", lat_deg)
    print("Longitude (deg):", lon_deg)
    print("Altitude (km):", alt_km)
    print("ECEF Position (km):")
    print("  X:", round(ecef[0], 3))
    print("  Y:", round(ecef[1], 3))
    print("  Z:", round(ecef[2], 3))


if __name__ == "__main__":
    main()

