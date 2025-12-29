# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Space weather data ingestion (NOAA SWPC)
#
# Supports ingestion of daily F10.7 solar flux and
# geomagnetic Ap index for use in atmospheric drag
# modeling and long-term orbit analysis.
#
# Reference:
#   Vallado, Fundamentals of Astrodynamics and Applications
#   NOAA SWPC documentation

from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class SpaceWeatherRecord:
    mjd: int
    f107: float
    ap: float


class SpaceWeatherTable:
    """
    Thread-safe table of space weather parameters.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._records: Dict[int, SpaceWeatherRecord] = {}

    def load_noaa_daily(self, path: str) -> None:
        """
        Load NOAA daily space weather data file.

        Expected format (example):
            YYYY MM DD F10.7 Ap

        Parameters
        ----------
        path : str
            Path to NOAA space weather file
        """
        with self._lock:
            with open(path, "r", encoding="ascii", errors="ignore") as f:
                for line in f:
                    parts = line.split()
                    if len(parts) < 5:
                        continue
                    try:
                        year = int(parts[0])
                        month = int(parts[1])
                        day = int(parts[2])
                        f107 = float(parts[3])
                        ap = float(parts[4])
                    except ValueError:
                        continue

                    # Convert calendar date to MJD
                    mjd = _calendar_to_mjd(year, month, day)

                    self._records[mjd] = SpaceWeatherRecord(
                        mjd=mjd,
                        f107=f107,
                        ap=ap,
                    )

    def get(self, mjd: int) -> Optional[SpaceWeatherRecord]:
        """
        Retrieve space weather record for given MJD.

        Parameters
        ----------
        mjd : int

        Returns
        -------
        SpaceWeatherRecord or None
        """
        with self._lock:
            return self._records.get(mjd)


def _calendar_to_mjd(year: int, month: int, day: int) -> int:
    """
    Convert calendar date to Modified Julian Date.

    This is a minimal internal utility to avoid
    external dependencies.
    """
    if month <= 2:
        year -= 1
        month += 12

    a = year // 100
    b = 2 - a + a // 4

    jd = int(
        365.25 * (year + 4716)
        + 30.6001 * (month + 1)
        + day
        + b
        - 1524.5
    )

    return jd - 2400000


# Global default space weather table
DEFAULT_SPACE_WEATHER = SpaceWeatherTable()

