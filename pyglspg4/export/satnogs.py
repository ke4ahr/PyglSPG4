# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SatNOGS observation export
#
# Generates SatNOGS-compatible observation schedules
# from predicted satellite passes.
#
# Reference:
#   https://wiki.satnogs.org/Observation_API

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass(frozen=True)
class SatNOGSObservation:
    """
    SatNOGS observation description.
    """
    norad_cat_id: int
    start_time: str          # ISO-8601 UTC
    end_time: str            # ISO-8601 UTC
    frequency: Optional[int] # Hz
    mode: Optional[str]
    description: Optional[str] = None


def export_satnogs(
    observations: List[SatNOGSObservation],
    path: str,
) -> None:
    """
    Export SatNOGS observations to a JSON file.

    Parameters
    ----------
    observations : list of SatNOGSObservation
        Observation windows to export
    path : str
        Output JSON file path
    """

    payload = {
        "observations": [asdict(obs) for obs in observations]
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

