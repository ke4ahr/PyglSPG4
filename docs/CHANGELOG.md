# Changelog

Copyright (C) 2025-2026 Kris Kirby, KE4AHR  
SPDX-License-Identifier: LGPL-3.0-or-later

All notable changes to this project are documented in this file.

This project follows a date-based versioning and milestone tracking
model aligned with scientific capability rather than semantic versioning.

---

## [2025-12-22]

### Added

- Complete project architecture definition
- Deterministic, thread-safe core design
- TLE parsing and validation
- Julian date and epoch handling
- Near-Earth SGP-4 implementation
- Mean motion recovery and drag modeling (B*)
- J2 secular perturbations
- Kepler equation solver
- TEME coordinate propagation
- TEME → PEF → ITRF frame transformations
- WGS-84 geodetic conversion
- Ground station geometry and topocentric coordinates
- AOS / LOS / max elevation pass prediction
- Integration test using ISS TLE
- Unit tests for math, parsing, and pass logic
- Explicit CAVEATS documentation
- Roadmap and architectural documentation

### Changed

- Clarified scope and limitations of SGP-4 vs SDP-4
- Explicit separation of near-Earth and deep-space propagation
- Documented missing scientific components transparently

### Deferred

- Full SDP-4 deep-space propagation
- Lunar–solar perturbations
- GEO / Molniya orbit support
- IERS Earth Orientation Parameters ingestion
- Precession / nutation modeling
- Doppler shift computation
- CAT (rigctl / Hamlib) integration
- SatNOGS export
- Covariance propagation
- Space-weather-driven atmospheric drag

### Fixed

- None (initial documented implementation)

---

## Planned

Future releases will address deferred items in alignment with
the project roadmap and validation goals.

