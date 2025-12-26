# Validation Strategy and Test Coverage

Copyright (C) 2025-2026 Kris Kirby, KE4AHR  
SPDX-License-Identifier: LGPL-3.0-or-later

---

## Purpose

This document describes the validation methodology, current test coverage,
and known gaps in the scientific verification of PyglSPG4.

The goal is to provide a clear path toward **numerical correctness,
determinism, and eventual parity with the NORAD / Vallado SGP-4 reference
implementation**.

---

## 1. Validation Philosophy

PyglSPG4 follows a layered validation approach:

- Unit-level mathematical correctness
- Integration-level orbital consistency
- Regression stability across time
- Reference comparison against authoritative sources

Validation emphasizes:
- Determinism
- Repeatability
- Explicit error bounding
- Transparent disclosure of limitations

---

## 2. Unit Testing

### 2.1 Math and Numerics

Covered:
- Vector operations
- Angle normalization
- Kepler equation solver convergence
- Numerical stability of trigonometric operations

Representative files:
- math/vectors.py
- math/angles.py
- math/kepler.py

---

### 2.2 Time and Epoch Handling

Covered:
- Julian date conversion
- Epoch parsing from TLEs
- Time-step consistency

Representative files:
- time/julian.py
- time/epochs.py

---

### 2.3 TLE Parsing and Validation

Covered:
- Line checksum validation
- Field extraction and normalization
- Range checks on orbital elements

Representative files:
- tle/parser.py
- tle/validator.py

---

## 3. Integration Testing

### 3.1 Near-Earth SGP-4 Propagation

Covered:
- End-to-end propagation from TLE to TEME position
- Basic error-code handling
- Perigee decay detection

Limitations:
- Does not yet validate against Vallado reference outputs
- Accuracy verified qualitatively, not quantitatively

---

### 3.2 Ground Station Pass Prediction

Covered:
- ISS pass prediction over known locations
- AOS / LOS detection
- Elevation masking behavior

Representative test:
- tests/test_pass_prediction.py

---

## 4. Reference Validation (Planned)

The following authoritative reference sources are planned but not yet implemented:

- Vallado C++ SGP-4 test vectors
- NORAD published validation cases
- STK / Orekit cross-comparison
- Multi-decade propagation stability tests

These will be used to:
- Quantify absolute position error
- Measure long-term drift
- Validate drag modeling

---

## 5. Deep-Space Validation (SDP-4)

Current state:
- Not applicable (SDP-4 not yet implemented)

Planned:
- GEO resonance validation
- Molniya orbit stability
- Lunar–solar perturbation comparison

---

## 6. Determinism and Reproducibility

Design guarantees:
- No mutable global state
- Explicit state initialization
- Pure functions for propagation

Testing approach:
- Repeated identical runs produce bitwise-identical results
- Parallel execution produces identical outputs

---

## 7. Numerical Error Handling

Current behavior:
- Basic decay detection
- No explicit floating-point error bounds

Planned:
- Error growth tracking
- Covariance propagation
- Sensitivity analysis

---

## 8. Validation Status Summary

Implemented:
- Unit tests (math, time, parsing)
- Integration tests (SGP-4 near-Earth, passes)

Missing:
- Reference vector comparison
- Long-term regression tests
- Deep-space validation
- Formal certification

---

## 9. Certification Statement

PyglSPG4 does **not** claim:
- NORAD certification
- Mission-grade accuracy
- Safety-of-life suitability

All validation gaps are documented and tracked in:
- CAVEATS.md
- ROADMAP.md
- ARCHITECTURE.md

---

## 10. Contribution Guidelines for Validation

Contributions adding validation must include:
- Source citation
- Numerical comparison data
- Automated test coverage
- Clear acceptance criteria

