# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# SDP-4 deep-space secular effects integrator (dspace)
#
# This module implements the deep-space secular evolution
# of orbital elements for resonant and non-resonant orbits.
#
# References:
#   NORAD Spacetrack Report #3
#   Vallado et al., AIAA 2006-6753, Section 7.5

from __future__ import annotations

import math
from pyglspg4.sdp4.state import SDP4State

TWOPI = 2.0 * math.pi
DAY_MINUTES = 1440.0


def dspace(state: SDP4State, tsince: float) -> None:
    """
    Apply deep-space secular perturbations.

    Parameters
    ----------
    state : SDP4State
        Initialized deep-space state (modified in-place)
    tsince : float
        Minutes since epoch
    """

    # --- Time variables ---
    t = tsince
    ft = state.fasx2 * t
    theta = state.gsto + state.xfact * t

    # --- Resonance handling ---
    if state.irez == 0:
        # ------------------------------------------------------------
        # Non-resonant secular evolution
        # ------------------------------------------------------------
        state.mean_anomaly += state.xmdot * t
        state.arg_perigee += state.omgdot * t
        state.raan += state.xnodot * t
        state.mean_motion += state.xndot * t

    else:
        # ------------------------------------------------------------
        # Resonant orbits (GEO or Molniya)
        # ------------------------------------------------------------
        atime = state.atime
        xli = state.xli
        xni = state.xni

        delt = 720.0  # integration step (minutes)

        # Integrate from previous time to now
        while abs(t - atime) >= delt:
            if t > atime:
                step = delt
            else:
                step = -delt

            # Resonance equations
            if state.irez == 1:
                # GEO (1-day resonance)
                xndot = (
                    state.d2201 * math.sin(xli - state.fasx2) +
                    state.d2211 * math.sin(xli) +
                    state.d3210 * math.sin(2.0 * xli) +
                    state.d3222 * math.sin(2.0 * (xli - state.fasx2))
                )
            else:
                # Molniya (½-day resonance)
                xndot = (
                    state.d4410 * math.sin(xli - 2.0 * state.fasx2) +
                    state.d4422 * math.sin(2.0 * (xli - state.fasx2)) +
                    state.d5220 * math.sin(xli) +
                    state.d5232 * math.sin(2.0 * xli)
                )

            xnddt = xndot * step
            xli += (xni + xnddt * 0.5) * step
            xni += xnddt

            atime += step

        # Final partial step
        dt = t - atime
        if abs(dt) > 0.0:
            if state.irez == 1:
                xndot = (
                    state.d2201 * math.sin(xli - state.fasx2) +
                    state.d2211 * math.sin(xli) +
                    state.d3210 * math.sin(2.0 * xli) +
                    state.d3222 * math.sin(2.0 * (xli - state.fasx2))
                )
            else:
                xndot = (
                    state.d4410 * math.sin(xli - 2.0 * state.fasx2) +
                    state.d4422 * math.sin(2.0 * (xli - state.fasx2)) +
                    state.d5220 * math.sin(xli) +
                    state.d5232 * math.sin(2.0 * xli)
                )

            xnddt = xndot * dt
            xli += (xni + xnddt * 0.5) * dt
            xni += xnddt

        # Save back
        state.atime = t
        state.xli = xli
        state.xni = xni

        # Recover mean elements
        state.mean_motion = xni
        state.mean_anomaly = (xli - theta) % TWOPI

    # --- Normalize angles ---
    state.mean_anomaly %= TWOPI
    state.arg_perigee %= TWOPI
    state.raan %= TWOPI

