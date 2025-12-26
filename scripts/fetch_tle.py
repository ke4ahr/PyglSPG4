# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Script: Fetch current TLEs from an online source.
# This example uses Celestrak's public TLE endpoints.

import urllib.request


CELESTRAK_ISS_URL = "https://celestrak.org/NORAD/elements/stations.txt"


def fetch_tle(url=CELESTRAK_ISS_URL):
    """
    Fetch TLE data from a remote URL.

    Returns
    -------
    list of str
        Raw lines of TLE data
    """

    with urllib.request.urlopen(url, timeout=10) as response:
        data = response.read().decode("utf-8")

    lines = [line.strip() for line in data.splitlines() if line.strip()]
    return lines


def main():
    lines = fetch_tle()
    print("Fetched", len(lines), "lines of TLE data")
    for line in lines[:6]:
        print(line)


if __name__ == "__main__":
    main()

