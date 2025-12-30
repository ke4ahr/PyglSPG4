# PyglSPG4 Architecture

Copyright (C) 2025-2026 Kris Kirby, KE4AHR  
SPDX-License-Identifier: LGPL-3.0-or-later

---

## 1. Overview

PyglSPG4 is a **full NORAD-grade implementation of SGP-4 and SDP-4 orbital propagation** in Python, designed for:

- Scientific correctness
- Deterministic, thread-safe execution
- Parallel propagation
- Ham-radio and ground-station operations
- Long-term maintainability

The project provides a **clean-room, file-by-file implementation** of the NORAD models as documented by Vallado et al., with extensions for modern operational use (frames, passes, Doppler, SatNOGS, CAT control).

---

## 2. Design Goals

- Full SGP-4 / SDP-4 parity with NORAD reference
- Deterministic and reproducible results
- No hidden global state
- Thread-safe and multiprocessing-safe
- Backend-agnostic math (native Python or NumPy)
- Clear separation between physics, numerics, and operations
- GitHub-safe, LGPL-compliant codebase

---

## 3. High-Level Architecture

The system is divided into layered subsystems:

1. Core Math & Time
2. TLE Handling
3. SGP-4 / SDP-4 Propagation
4. Frames & Earth Orientation
5. Ground Station & Visibility
6. Operational Outputs (Doppler, CAT, SatNOGS)
7. Validation & Testing
8. Examples & Scripts

Each layer depends only on layers below it.

---

## 4. Package Layout

    pyglspg4/
        api/
            propagate.py
            batch.py
            parallel.py
            vectorized.py
            exceptions.py

        backend/
            base.py
            python.py
            numpy.py
            selector.py

        constants.py

        math/
            numerics.py
            vectors.py
            rotations.py

        time/
            julian.py
            epochs.py

        tle/
            parser.py
            validator.py

        sgp4/
            state.py
            initializer.py
            near_earth.py
            propagate.py

        sdp4/
            constants.py
            state.py
            resonance.py
            solar_lunar.py
            integrator.py
            periodic.py
            eci.py
            propagate.py

        frames/
            teme.py
            ecef.py
            itrf.py
            eop.py

        groundstation/
            station.py
            visibility.py
            pass_prediction.py

        export/
            frequency_tables.py
            satnogs.py

        radio/
            doppler.py
            cat.py

        validation/
            reference.py
            determinism.py
            regression.py

    examples/
        iss_passes_alabama.py
        doppler_table_iss.py
        satnogs_export.py

    docs/
        ARCHITECTURE.md
        MANPAGE.md
        VALIDATION.md
        CHANGELOG.md
        CAVEATS.md

    tests/
        test_constants.py
        test_sgp4.py
        test_sdp4.py
        test_frames.py
        test_groundstation.py

---

## 5. Core Constants and Units

All physical constants are defined centrally in `pyglspg4/constants.py`, including:

- XKE
- AE
- CK2
- CK4
- QOMS2T
- S
- Earth radius
- Earth rotation rate

Units follow NORAD conventions:
- Distance: Earth radii internally, km externally
- Time: minutes from epoch
- Angles: radians internally

---

## 6. Math and Numerics Layer

### 6.1 Vectors and Rotations

- Immutable vector operations
- Explicit rotation matrices
- No reliance on global state

### 6.2 Backend Selection

The backend system allows switching between:

- Pure Python math
- NumPy vectorized math

Backend selection is explicit and thread-safe.

---

## 7. Time System

Time handling includes:

- Julian date conversion
- UTC, TAI, TT separation
- Epoch handling consistent with TLE format

All propagation is performed in **minutes since epoch**.

---

## 8. TLE Handling

### 8.1 Parsing

- Strict fixed-column parsing
- Checksum verification
- Field validation

### 8.2 Validation

- Mean motion bounds
- Eccentricity bounds
- Inclination bounds
- NORAD catalog consistency

Invalid TLEs raise explicit exceptions.

---

## 9. SGP-4 Implementation (Near-Earth)

### 9.1 Initialization

- Drag terms
- Secular rates
- Deep-space switch determination

### 9.2 Propagation

- Secular updates
- Periodic perturbations
- Atmospheric drag
- Error codes per NORAD specification

---

## 10. SDP-4 Implementation (Deep Space)

### 10.1 Resonance Handling

- 1:1 (GEO)
- 2:1 (Molniya)

### 10.2 Solar-Lunar Perturbations

- Third-body gravity
- Long-period effects

### 10.3 Numerical Integration

- Stepwise integration
- Stability-controlled updates
- Time-varying drag support

---

## 11. Frames & Earth Orientation

Implemented frames:

- TEME
- ECEF
- ITRF

Features:

- Earth rotation
- Polar motion
- IERS EOP ingestion
- UTC-based transforms

---

## 12. Ground Station & Pass Prediction

### 12.1 Ground Station Model

- WGS-84 ellipsoid
- Geodetic to ECEF conversion

### 12.2 Visibility

- Elevation masking
- Atmospheric refraction correction

### 12.3 Pass Prediction

- AOS / LOS detection
- Max elevation computation
- Deterministic pass segmentation

---

## 13. Radio & Operations

### 13.1 Doppler Correction

- Relativistic Doppler computation
- Frequency tables
- Time-resolved sweeps

### 13.2 CAT Control

- rigctl / Hamlib compatibility
- Frequency steering
- Safe external process control

---

## 14. SatNOGS Export

- JSON-compatible observation export
- Start/stop times in UTC
- Frequency and mode metadata
- Scheduler-ready output

---

## 15. Parallelism & Thread Safety

- No global mutable state
- Stateless propagation functions
- Safe multiprocessing and threading
- Deterministic batch execution

---

## 16. Validation & Testing

### 16.1 Reference Validation

- Vallado test vectors
- NORAD reference outputs
- Tolerance-based comparison

### 16.2 Determinism

- Repeatability checks
- Parallel invariance

### 16.3 Regression

- Long-term drift detection
- GEO and Molniya stability tests

---

## 17. Examples

Included runnable examples demonstrate:

- ISS pass prediction over Alabama
- Doppler table generation
- SatNOGS export workflows

---

## 18. Caveats

- Atmospheric models beyond NORAD are optional extensions
- Space weather ingestion is supported but not required
- Visualization is optional and external

Refer to `docs/CAVEATS.md` for details.

---

## 19. Licensing

PyglSPG4 is licensed under:

- GNU Lesser General Public License v3.0 or later
- SPDX identifier: LGPL-3.0-or-later

All files include appropriate copyright headers.

---

## 20. Status

As of 2025-12-22:

- Full SGP-4 / SDP-4 implemented
- Validation complete
- Operational features complete
- Ready for scientific and amateur-radio use

---

