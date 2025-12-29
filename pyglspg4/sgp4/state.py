# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SGP-4 state container
#
# This module defines the SGP4State dataclass which stores
# all precomputed constants, secular rates, and runtime
# parameters required by SGP-4 / SDP-4 propagation.
#
# References:
#   NORAD Spacetrack Report #3
#   Vallado et al., AIAA 2006-6753

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class SGP4State:
    """
    Container for SGP-4 / SDP-4 propagation state.

    All values are stored in canonical SGP-4 units
    unless otherwise specified.

    Angles are in radians.
    Time is in minutes.
    Distances are in Earth radii (AE) unless noted.
    """

    # ------------------------------------------------------------------
    # Initialization status
    # ------------------------------------------------------------------
    initialized: bool = False
    is_deep_space: bool = False

    # ------------------------------------------------------------------
    # TLE-derived elements (epoch values)
    # ------------------------------------------------------------------
    epoch_jd: float = 0.0

    inclination: float = 0.0          # radians
    raan: float = 0.0                 # right ascension of ascending node
    eccentricity: float = 0.0
    arg_perigee: float = 0.0
    mean_anomaly: float = 0.0
    mean_motion: float = 0.0          # radians / minute

    bstar: float = 0.0                # drag term

    # ------------------------------------------------------------------
    # Derived orbital quantities
    # ------------------------------------------------------------------
    semi_major_axis: float = 0.0       # Earth radii
    perigee_radius: float = 0.0        # Earth radii
    apogee_radius: float = 0.0         # Earth radii

    # ------------------------------------------------------------------
    # Secular rates (rad / min, rad / min^2)
    # ------------------------------------------------------------------
    xmdot: float = 0.0
    omgdot: float = 0.0
    xnodot: float = 0.0

    xnodcf: float = 0.0
    t2cof: float = 0.0
    xlcof: float = 0.0
    aycof: float = 0.0
    delmo: float = 0.0
    sinmo: float = 0.0

    # ------------------------------------------------------------------
    # Drag and atmospheric coefficients
    # ------------------------------------------------------------------
    cc1: float = 0.0
    cc4: float = 0.0
    cc5: float = 0.0

    d2: float = 0.0
    d3: float = 0.0
    d4: float = 0.0

    # ------------------------------------------------------------------
    # Near-Earth periodic terms
    # ------------------------------------------------------------------
    eta: float = 0.0
    beta: float = 0.0
    omgcof: float = 0.0
    xmcof: float = 0.0

    # ------------------------------------------------------------------
    # Deep-space placeholders (SDP-4)
    # ------------------------------------------------------------------
    deep_space_state: Optional[object] = None

    # ------------------------------------------------------------------
    # Runtime flags / diagnostics
    # ------------------------------------------------------------------
    error_code: int = 0

    # ------------------------------------------------------------------
    # Utility methods
    # ------------------------------------------------------------------
    def reset_errors(self) -> None:
        """Clear any stored error condition."""
        self.error_code = 0

    def mark_initialized(self, deep_space: bool) -> None:
        """Mark the state as initialized."""
        self.initialized = True
        self.is_deep_space = deep_space

    def validate(self) -> None:
        """
        Validate state consistency.

        Raises
        ------
        ValueError if state is invalid.
        """
        if not self.initialized:
            raise ValueError("SGP4State is not initialized")

        if self.semi_major_axis <= 0.0:
            raise ValueError("Invalid semi-major axis")

        if not (0.0 <= self.eccentricity < 1.0):
            raise ValueError("Eccentricity out of range")

        if self.mean_motion <= 0.0:
            raise ValueError("Invalid mean motion")

        if abs(self.inclination) > 3.2:
            raise ValueError("Inclination out of expected bounds")

