# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Example: Batch propagation of multiple satellites.

from datetime import datetime
from pyglspg4.tle.parser import parse_tle
from pyglspg4.api.propagate import propagate


TLES = [
    (
        "1 25544U 98067A   24001.51869444  .00016717  00000-0  10270-3 0  9991",
        "2 25544  51.6405  24.4561 0004382  88.1684  38.3275 15.49745126398784",
    ),
]


def main():
    tles = [parse_tle(l1, l2) for l1, l2 in TLES]
    now = datetime.utcnow()

    print("Batch propagation at:", now.isoformat(), "UTC")

    for tle in tles:
        pos, vel, err = propagate(tle, 0.0)
        if err == 0:
            print("Position (km):", tuple(round(x, 3) for x in pos))
        else:
            print("Propagation error:", err)


if __name__ == "__main__":
    main()

