# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Ground station definition and topocentric transforms.

import math


class GroundStation:
    """
    Ground station defined by geodetic coordinates.
    """

    def __init__(self, lat_rad, lon_rad, alt_km):
        self.lat = lat_rad
        self.lon = lon_rad
        self.alt = alt_km

        self._sin_lat = math.sin(lat_rad)
        self._cos_lat = math.cos(lat_rad)
        self._sin_lon = math.sin(lon_rad)
        self._cos_lon = math.cos(lon_rad)

    def ecef_position(self):
        """
        Ground station ECEF (ITRF) position in km.
        """

        a = 6378.137
        f = 1.0 / 298.257223563
        e2 = f * (2.0 - f)

        N = a / math.sqrt(1.0 - e2 * self._sin_lat * self._sin_lat)

        x = (N + self.alt) * self._cos_lat * self._cos_lon
        y = (N + self.alt) * self._cos_lat * self._sin_lon
        z = (N * (1.0 - e2) + self.alt) * self._sin_lat

        return (x, y, z)

    def topocentric(self, sat_itrf_km):
        """
        Compute topocentric coordinates (range, azimuth, elevation).

        Parameters
        ----------
        sat_itrf_km : tuple(float, float, float)
            Satellite ECEF position

        Returns
        -------
        (range_km, az_rad, el_rad)
        """

        xs, ys, zs = sat_itrf_km
        xg, yg, zg = self.ecef_position()

        dx = xs - xg
        dy = ys - yg
        dz = zs - zg

        # ENU rotation
        east = -self._sin_lon * dx + self._cos_lon * dy
        north = (
            -self._sin_lat * self._cos_lon * dx
            - self._sin_lat * self._sin_lon * dy
            + self._cos_lat * dz
        )
        up = (
            self._cos_lat * self._cos_lon * dx
            + self._cos_lat * self._sin_lon * dy
            + self._sin_lat * dz
        )

        rng = math.sqrt(east * east + north * north + up * up)
        az = math.atan2(east, north) % (2.0 * math.pi)
        el = math.asin(up / rng)

        return rng, az, el

