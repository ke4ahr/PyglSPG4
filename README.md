# PyglSPG4

Copyright (C) 2025-2026 Kris Kirby, KE4AHR  
SPDX-License-Identifier: LGPL-3.0-or-later

---

## Overview

PyglSPG4 is a **pure-Python implementation of the NORAD SGP-4 / SDP-4 satellite
orbit propagation models**, designed with an emphasis on:

- Deterministic, thread-safe execution
- Clear scientific architecture
- Amateur radio satellite operations
- Educational and research use
- LGPL-3.0-or-later licensing

The project is intentionally transparent about its current capabilities
and limitations, with all gaps explicitly documented.

---

## Key Features

- TLE parsing and validation
- Near-Earth SGP-4 orbital propagation
- TEME → Earth-fixed frame transformations
- Ground-station geometry and visibility
- Satellite pass prediction (AOS / LOS / max elevation)
- Deterministic, parallel-safe design
- Optional NumPy acceleration
- Extensive documentation and caveats

---

## Supported Orbits

- Near-Earth satellites (orbital period < 225 minutes)

Deep-space orbits (GEO, Molniya, Tundra) are **architecturally planned**
but **not yet implemented**.

---

## Installation

From source:

    git clone https://github.com/ke4ahr/Pyglspg4.git
    cd Pyglspg4
    pip install .

Optional NumPy support:

    pip install .[numpy]

Development dependencies:

    pip install .[dev]

---

## Basic Usage

### Propagating a Satellite Orbit

    from pyglspg4.tle.parser import parse_tle
    from pyglspg4.api.propagate import propagate

    tle = parse_tle(line1, line2)
    position_km, velocity_km_s, error = propagate(tle, tsince_min)

    if error == 0:
        print(position_km)
    else:
        print("Propagation error:", error)

---

### Predicting Ground-Station Passes

    from datetime import datetime, timedelta
    import math

    from pyglspg4.groundstation.station import GroundStation
    from pyglspg4.groundstation.passes import predict_passes

    lat = math.radians(32.806671)
    lon = math.radians(-86.791130)
    alt_km = 0.2

    station = GroundStation(lat, lon, alt_km)

    start = datetime.utcnow()
    end = start + timedelta(days=2)

    passes = predict_passes(tle, station, start, end)

    for p in passes:
        print(p["aos"], p["los"], p["max_el"])

---

## Examples and Scripts

See the `examples/` and `scripts/` directories for:

- ISS pass prediction
- Ground-station geometry
- Batch propagation
- Fetching live TLEs
- Printing pass tables

---

## Documentation

Detailed documentation is provided in the `docs/` directory:

- ARCHITECTURE.md — system design and philosophy
- ROADMAP.md — planned features and phases
- VALIDATION.md — test coverage and validation strategy
- CAVEATS.md — scientific limitations and gaps
- CHANGELOG.md — project history
- MANPAGE.md — user-facing manual

---

## Scientific Status

Current state:

- SGP-4 near-Earth: implemented and usable
- SDP-4 deep-space: not yet implemented
- Earth orientation: simplified (GMST only)
- Validation: partial, not NORAD-certified

This software **does not claim mission-grade accuracy**.

See `docs/CAVEATS.md` for full disclosure.

---

## Intended Use

PyglSPG4 is intended for:

- Amateur radio satellite tracking
- Educational orbital mechanics
- Research prototyping
- Non-safety-critical applications

It is **not intended** for:

- Mission planning
- Collision avoidance
- Spaceflight operations
- Safety-of-life systems

---

## License

PyglSPG4 is licensed under the **GNU Lesser General Public License v3.0
or later (LGPL-3.0-or-later)**.

You may use this library in proprietary applications provided that
modifications to the library itself are released under the same license.

See the `LICENSE` file for full terms.

---

## Author

Kris Kirby, KE4AHR

---

## Contributing

Contributions are welcome.

Please ensure that any contribution includes:

- Clear scientific justification
- Unit and integration tests
- Reference citations where applicable
- Compliance with LGPL-3.0-or-later

---

## Disclaimer

This software is provided “as is”, without warranty of any kind.

Use at your own risk.

