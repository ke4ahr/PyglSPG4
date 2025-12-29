# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SatNOGS export utilities
#
# Converts predicted satellite passes into SatNOGS-compatible
# observation request payloads.
#
# Reference:
#   https://wiki.satnogs.org/Observation

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import List

from pyglspg4.groundstation.pass_prediction import PassEvent


@dataclass(frozen=True)
class SatNOGSObservation:
    satellite_id: int
    start_time_utc: str
    end_time_utc: str
    azimuth_deg: float
    elevation_deg: float
    frequency_hz: float
    mode: str = "FM"
    bandwidth_hz: int = 12000
    polarization: str = "RHCP"


def export_satnogs_observations(
    passes: List[PassEvent],
    satellite_id: int,
    downlink_frequency_hz: float,
    path: str,
) -> None:
    """
    Export passes as SatNOGS observation JSON.

    Parameters
    ----------
    passes : list of PassEvent
        Predicted satellite passes
    satellite_id : int
        SatNOGS satellite catalog ID
    downlink_frequency_hz : float
        Nominal downlink frequency
    path : str
        Output JSON file
    """

    observations = []

    for p in passes:
        observations.append(
            SatNOGSObservation(
                satellite_id=satellite_id,
                start_time_utc=p.aos_utc.isoformat(),
                end_time_utc=p.los_utc.isoformat(),
                azimuth_deg=p.max_azimuth_deg,
                elevation_deg=p.max_elevation_deg,
                frequency_hz=downlink_frequency_hz,
            )
        )

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            [asdict(o) for o in observations],
            f,
            indent=2,
        )

