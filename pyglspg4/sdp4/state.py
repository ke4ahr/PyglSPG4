# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SDP-4 deep-space state container
# Mirrors NORAD deep-space common block (dscom / dsinit)

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class SDP4State:
    """
    Holds all deep-space perturbation parameters for SDP-4 propagation.

    This structure corresponds to the NORAD deep-space common variables
    used across dscom, dsinit, dspace, and dpper.
    """

    # Flags
    is_deep_space: bool = False
    resonance: bool = False
    synchronous: bool = False

    # Epoch-related
    epoch_jd: float = 0.0

    # Mean elements
    mean_motion: float = 0.0        # rad/min
    eccentricity: float = 0.0
    inclination: float = 0.0
    raan: float = 0.0
    arg_perigee: float = 0.0
    mean_anomaly: float = 0.0

    # Solar-lunar terms
    sse: float = 0.0
    ssi: float = 0.0
    ssl: float = 0.0
    ssg: float = 0.0
    ssh: float = 0.0
    ssd: float = 0.0

    # Periodic terms
    pe: float = 0.0
    pinc: float = 0.0
    pl: float = 0.0
    pgh: float = 0.0
    ph: float = 0.0

    # Resonance terms
    del1: float = 0.0
    del2: float = 0.0
    del3: float = 0.0
    fasx2: float = 0.0
    fasx4: float = 0.0
    fasx6: float = 0.0

    # Integration state
    atime: float = 0.0
    xli: float = 0.0
    xni: float = 0.0

    # Error tracking
    error: int = 0

    # -------------------------------------------------------------

    def reset(self) -> None:
        self.atime = 0.0
        self.xli = 0.0
        self.xni = self.mean_motion

    def has_error(self) -> bool:
        return self.error != 0

