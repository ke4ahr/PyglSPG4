PYGLSPG4(1)                     User Commands                    PYGLSPG4(1)

NAME
    pyglspg4 — Python implementation of NORAD SGP-4 / SDP-4 for satellite tracking

SYNOPSIS
    pyglspg4 [options]

DESCRIPTION
    PyglSPG4 is a pure-Python, LGPL-licensed implementation of the NORAD
    Simplified General Perturbations models (SGP-4 and SDP-4).

    It is designed for deterministic orbital propagation, ground-station
    visibility prediction, and amateur radio satellite operations.

    The software emphasizes architectural clarity, scientific transparency,
    and thread-safe execution.

FEATURES
    - TLE parsing and validation
    - Near-Earth SGP-4 orbital propagation
    - TEME → Earth-fixed coordinate transformations
    - Ground-station pass prediction (AOS / LOS / max elevation)
    - Deterministic and parallel-safe design

SUPPORTED ORBITS
    - Near-Earth satellites (period < 225 minutes)

    Deep-space orbits (GEO, Molniya, Tundra) are architecturally planned
    but not yet implemented.

COMMAND-LINE INTERFACE
    A formal command-line interface is planned but not yet finalized.

    Current usage is via the Python API.

PYTHON API OVERVIEW
    Basic propagation example:

        from pyglspg4.tle.parser import parse_tle
        from pyglspg4.api.propagate import propagate

        tle = parse_tle(line1, line2)
        pos, vel, err = propagate(tle, tsince_min)

    Ground-station pass prediction:

        from pyglspg4.groundstation.station import GroundStation
        from pyglspg4.groundstation.passes import predict_passes

        station = GroundStation(lat_rad, lon_rad, alt_km)
        passes = predict_passes(tle, station, start_dt, end_dt)

FILES
    sgp4/
        Near-Earth propagation core

    sdp4/
        Deep-space propagation (planned)

    frames/
        Coordinate frame transformations

    groundstation/
        Visibility and pass prediction

    docs/
        Architecture, validation, caveats, roadmap

LIMITATIONS
    - SDP-4 deep-space propagation not implemented
    - No IERS Earth Orientation Parameters ingestion
    - No Doppler shift or CAT control
    - No formal NORAD certification

    See CAVEATS.md for full details.

LICENSE
    GNU Lesser General Public License v3.0 or later (LGPL-3.0-or-later)

AUTHOR
    Kris Kirby, KE4AHR

DISCLAIMER
    This software is provided "as is" without warranty of any kind.

    It is intended for educational, research, and amateur radio use.
    It is not certified for mission-critical or safety-of-life applications.

SEE ALSO
    CAVEATS.md
    ARCHITECTURE.md
    ROADMAP.md
    VALIDATION.md

