# CAVEATS AND SCIENTIFIC LIMITATIONS

Copyright (C) 2025-2026 Kris Kirby, KE4AHR  
SPDX-License-Identifier: LGPL-3.0-or-later

---

## Overview

This document enumerates **known scientific, numerical, and standards-related limitations**
of the current PyglSPG4 implementation.

The intent is **full transparency**: this software is architecturally correct, testable,
and usable for amateur and research purposes, but it does **not yet claim full NORAD /
Vallado reference parity**.

---

## 1. Core Orbital Propagation

### 1.1 SGP-4 (Near-Earth)

Implemented:
- Mean motion recovery
- Atmospheric drag (static B*)
- J2 secular perturbations
- Kepler solver
- TEME position output
- Perigee decay detection

Missing / Partial:
- Full CK4 secular terms
- Higher-order short-period corrections
- Time-varying drag modeling
- Numerical equivalence verification against Vallado C++ to < 1 mm

Status:
- Suitable for LEO tracking and pass prediction
- Not certified for precision orbit determination

---

### 1.2 SDP-4 (Deep-Space)

Current State:
- **NOT fully implemented**

Missing:
- Deep-space resonance integrator
- Lunar–solar third-body perturbations
- Long-period and short-period corrections
- GEO / Molniya drift modeling
- Time-dependent drag coupling

Impact:
- Deep-space TLEs (period > 225 minutes) are **not valid**
- GEO, Tundra, Molniya orbits are unsupported

---

## 2. Frames and Earth Orientation

Implemented:
- TEME → PEF (GMST only)
- PEF → ITRF with static polar motion
- ITRF → geodetic conversion

Missing:
- IERS EOP ingestion (xp, yp, DUT1)
- UT1–UTC handling
- Velocity frame transformations
- Precession / nutation (IAU-2000/2006)

Impact:
- Sub-meter errors accumulate over days
- Velocity vectors are incomplete in ECEF

---

## 3. Ground Station & Pass Prediction

Implemented:
- Topocentric range / azimuth / elevation
- AOS / LOS / max elevation detection
- Configurable elevation masks

Missing:
- Atmospheric refraction correction
- Earth shadow / eclipse modeling
- RF horizon modeling
- Slant-range Doppler computation

Impact:
- Pass timing is accurate to seconds
- Elevation near horizon is optimistic

---

## 4. Atmospheric Modeling

Implemented:
- NORAD-standard exponential atmosphere
- Static B* drag term

Missing:
- Space-weather driven density models
- NOAA SWPC data ingestion
- MSIS / JB2008 models
- Drag coefficient evolution

Impact:
- Long-term orbit decay inaccurate
- Short-term passes unaffected

---

## 5. Radio & Ham Integration

Implemented:
- None

Missing:
- Doppler shift computation
- Automatic frequency correction tables
- CAT control (rigctl / Hamlib)
- APRS / digipeater support

Impact:
- Manual radio tuning required

---

## 6. Validation & Certification

Implemented:
- Unit tests for parsing, math, passes
- Basic integration tests

Missing:
- Vallado reference test vectors
- Regression tests across decades
- Covariance propagation
- Error growth characterization

Impact:
- No formal certification claim
- Scientific validation incomplete

---

## 7. Visualization & Outputs

Implemented:
- None (core math only)

Missing:
- Ground-track plotting
- Pass elevation plots
- GEO / Molniya drift plots
- 3D orbit visualization

---

## 8. Intended Use Disclaimer

This software is intended for:
- Amateur radio satellite tracking
- Educational orbital mechanics
- Research prototyping
- Non-safety-critical applications

This software is **NOT** intended for:
- Mission planning
- Collision avoidance
- Spaceflight operations
- NORAD-equivalent orbit determination

---

## 9. Roadmap Alignment

All missing items are explicitly tracked in:
- ARCHITECTURE.md
- ROADMAP.md
- CHANGELOG.md

Contributions addressing these caveats are welcome.

