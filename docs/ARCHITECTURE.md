# PyglSPG4 Architecture

Copyright (C) 2025-2026 Kris Kirby, KE4AHR  
SPDX-License-Identifier: LGPL-3.0-or-later

---

## 1. Architectural Goals

PyglSPG4 is a pure-Python, LGPL-licensed implementation of NORAD SGP-4 / SDP-4 designed for:

- Deterministic orbital propagation
- Thread-safe and parallel execution
- Clear separation of physics, math, frames, and I/O
- Ham-radio satellite operations
- Scientific extensibility

Primary design references:
- Vallado, D. A., Fundamentals of Astrodynamics and Applications
- NORAD SGP-4 / SDP-4 reference implementation

---

## 2. Layered Design Overview

    API Layer
     ├── propagate()
     ├── batch / vectorized
     └── parallel execution

    Propagation Core
     ├── SGP-4 (Near-Earth)
     └── SDP-4 (Deep-Space)

    Physics & Math
     ├── Kepler solvers
     ├── Vector algebra
     └── Numerical utilities

    Frames & Time
     ├── TEME → PEF → ITRF
     ├── Geodetic transforms
     └── Julian / epoch handling

    Ground Systems
     ├── Ground station geometry
     ├── Pass prediction
     └── Visibility modeling

    Validation & Tests
     ├── Unit tests
     ├── Integration tests
     └── Reference comparisons

---

## 3. Core Orbital Propagation

### 3.1 SGP-4 (Near-Earth)

Implemented components:
- Mean motion recovery
- Drag modeling (B*)
- J2 secular perturbations
- Kepler equation solver
- Perigee decay handling

Key files:
- sgp4/initializer.py
- sgp4/near_earth.py
- sgp4/state.py

Design choice:
- Stateless propagation functions
- Immutable initialized state
- No global variables

---

### 3.2 SDP-4 (Deep-Space)

Current status:
- Architectural placeholders present
- Full physics not yet implemented

Required components:
- Deep-space resonance integrator
- Lunar–solar perturbations
- Long-period corrections
- Short-period corrections
- GEO / Molniya orbit handling

Planned files:
- sdp4/integrator.py
- sdp4/solar_lunar.py
- sdp4/resonance.py
- sdp4/periodic.py

---

## 4. Frames & Earth Orientation

Implemented:
- TEME → PEF using GMST
- PEF → ITRF with static polar motion
- ITRF → geodetic conversion (WGS-84)

Missing:
- IERS EOP ingestion (xp, yp, DUT1)
- UT1–UTC correction handling
- Precession and nutation (IAU-2000/2006)
- Velocity frame transformations

Key files:
- frames/gmst.py
- frames/teme_to_pef.py
- frames/pef_to_itrf.py
- frames/itrf_to_geodetic.py

---

## 5. Ground Station & Pass Prediction

Implemented:
- Ground station definition (lat, lon, alt)
- Topocentric ENU conversion
- Range, azimuth, elevation
- AOS / LOS / maximum elevation detection
- Elevation masking

Key files:
- groundstation/station.py
- groundstation/passes.py

Planned extensions:
- Atmospheric refraction correction
- Doppler shift computation
- RF horizon modeling
- Visibility quality metrics

---

## 6. Parallelism & Thread Safety

Design guarantees:
- No mutable global state
- Immutable state objects
- Pure propagation functions

Supported execution models:
- Single-threaded deterministic runs
- multiprocessing-based batch execution
- concurrent.futures executors
- Optional NumPy vectorization backend

---

## 7. Validation Strategy

Implemented:
- Unit tests for parsing, math utilities, and passes
- Integration test using ISS TLE

Missing:
- Vallado reference test vector suite
- Long-term GEO / Molniya drift validation
- Covariance propagation
- Numerical error growth analysis

Directories:
- tests/
- validation/

---

## 8. Packaging & Distribution

Target characteristics:
- PyPI-distributable package
- Optional NumPy acceleration
- Minimal runtime dependencies
- Clear LGPL compliance

Planned artifacts:
- pyproject.toml
- Semantic versioning
- Reproducible builds

---

## 9. Licensing

License:
- GNU LGPL v3.0 or later

Policy:
- SPDX identifiers in all source files
- Explicit copyright headers
- No copyleft contamination of downstream user code

---

## 10. Roadmap Summary

Short-term:
- Complete SDP-4 deep-space propagation
- Add IERS Earth Orientation ingestion
- Vallado parity testing

Mid-term:
- Doppler correction
- CAT / Hamlib integration
- SatNOGS export
- Visualization tools

Long-term:
- Covariance propagation
- Space-weather-driven drag modeling
- Formal scientific certification

---

## 11. Architectural Integrity Statement

This architecture is:

- Deterministic
- Thread-safe
- Modular
- Scientifically grounded

All remaining gaps are explicitly documented and bounded.

PyglSPG4 is currently suitable for:
- Amateur radio satellite tracking
- Educational orbital mechanics
- Research prototyping

Mission-critical or safety-of-life applications are explicitly out of scope at this time.

