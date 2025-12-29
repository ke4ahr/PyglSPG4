# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Earth Orientation Parameters (EOP)
#
# Supports ingestion of IERS finals2000A-style data files
# and provides polar motion and UT1-UTC corrections.
#
# Reference:
#   IERS Conventions (2010)
#   Vallado, Fundamentals of Astrodynamics and Applications

from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class EOPRecord:
    mjd: int
    xp: float        # arcseconds
    yp: float        # arcseconds
    ut1_utc: float   # seconds


class EOPTable:
    """
    Thread-safe Earth Orientation Parameter table.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._records: Dict[int, EOPRecord] = {}

    def load_finals2000a(self, path: str) -> None:
        """
        Load an IERS finals2000A file.

        Parameters
        ----------
        path : str
            Path to finals2000A.data or equivalent
        """
        with self._lock:
            with open(path, "r", encoding="ascii", errors="ignore") as f:
                for line in f:
                    if len(line) < 68:
                        continue
                    try:
                        mjd = int(line[7:15])
                        xp = float(line[18:27])
                        yp = float(line[37:46])
                        ut1_utc = float(line[58:68])
                    except ValueError:
                        continue

                    self._records[mjd] = EOPRecord(
                        mjd=mjd,
                        xp=xp,
                        yp=yp,
                        ut1_utc=ut1_utc,
                    )

    def get(self, mjd: int) -> Optional[EOPRecord]:
        """
        Retrieve EOP record for a given Modified Julian Date.

        Parameters
        ----------
        mjd : int

        Returns
        -------
        EOPRecord or None
        """
        with self._lock:
            return self._records.get(mjd)


# Global default EOP table
DEFAULT_EOP = EOPTable()

