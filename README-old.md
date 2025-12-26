# PyglSPG4

**Simplified General Perturbations-4 (SGP-4) implemented in Python under LGPL-3.0**

---

## Overview

**PyglSPG4** is a clean, modern Python implementation of the Simplified General Perturbations-4 (SGP-4) orbital propagator used for Earth-orbiting satellites. It propagates satellite position and velocity from Two-Line Element (TLE) sets with an emphasis on:

- Correctness and numerical fidelity  
- Thread safety and deterministic behavior  
- Parallel execution  
- Optional NumPy acceleration  
- LGPL-3.0-or-later licensing, enabling use in both open-source and proprietary systems  

This project is suitable for:

- Amateur and professional ground-station software  
- Space situational awareness (SSA)  
- Satellite simulation and analysis  
- Educational and research use  
- Batch propagation of large satellite catalogs  

---

## Project Goals

- Implement SGP-4 faithfully using a clean-room Python design  
- Support pure Python execution (zero required dependencies)  
- Support NumPy-accelerated execution for performance  
- Enable parallel batch propagation  
- Ensure thread safety using immutable state  
- Provide a maintainable and extensible codebase  
- Remain fully LGPL-3.0-or-later compliant  

---

## Features

- Full SGP-4 propagation model  
- Near-Earth and deep-space orbit handling  
- Immutable propagation state objects  
- Deterministic floating-point behavior  
- Dual math backends:
  - Native Python math
  - NumPy vectorized backend  
- Parallel propagation using threads or processes  
- Explicit error handling and validation  
- Designed for long-term extensibility  

---

## Installation

### From Source

    git clone https://github.com/ke4ahr/PyglSPG4.git
    cd PyglSPG4
    pip install -e .

### Dependencies

- Python 3.10 or newer  
- NumPy (optional, for accelerated backend)  

PyglSPG4 functions fully without NumPy.

---

## Basic Usage (Planned API)

### Parsing a TLE

    from pyglspg4 import parse_tle

    tle = [
        "1 25544U 98067A   25344.12345678  .00006789  00000-0  10270-4 0  9991",
        "2 25544  51.6452 123.4567 0007863  20.1234 340.9876 15.50012345  1234"
    ]

    state = parse_tle(tle)

### Propagating to an Epoch

    from pyglspg4 import propagate

    pv = propagate(state, epoch="2025-12-25T12:00:00Z")
    print(pv.position, pv.velocity)

### Selecting an Execution Backend

    from pyglspg4.backend import select_backend

    backend = select_backend(prefer="numpy")
    pv = propagate(state, epoch, backend=backend)

---

## Parallel Propagation

PyglSPG4 supports batch propagation across:

- Multiple satellites  
- Multiple epochs  
- Threads or processes  
- NumPy vectorized execution  

Example:

    from pyglspg4 import batch

    results = batch(states, epochs, backend="numpy", strategy="process")

---

## Thread Safety and Determinism

- No global mutable state  
- All propagation inputs are immutable  
- Numerical routines are pure functions  
- Safe concurrent execution  
- Reproducible results across runs  

---

## Testing and Validation

Planned validation strategy includes:

- Reference vectors from Vallado and NASA SGP-4  
- Cross-backend comparison tests  
- Regression testing against known catalogs  
- Deterministic parallel execution tests  

---

## Project Status

Early development and architecture phase.

- Core architecture defined  
- Public API under active design  
- Math implementation in progress  
- No official release yet  

---

## Roadmap

### Phase 1 — Core Implementation

- Implement reference-aligned SGP-4 math  
- TLE parsing and validation  
- Scalar propagation using pure Python backend  
- Unit tests for all math primitives  

### Phase 2 — Performance and Parallelism

- NumPy backend implementation  
- Vectorized Kepler solver  
- Parallel batch propagation  
- Performance benchmarking harness  

### Phase 3 — Stability and Release

- Full validation against reference outputs  
- Deterministic regression tests  
- API freeze  
- Version 1.0.0 release  

### Phase 4 — Extended Capabilities

- SDP-4 deep-space refinements  
- Earth orientation parameter support  
- Optional GPU acceleration using Numba or CUDA  
- Command-line propagation tool  

### Long-Term Vision

- Real-time TLE ingestion  
- Large-scale SSA pipelines  
- Interoperability with SDR and ground-station software  
- Optional language bindings and accelerators  

---

## Contributing

Contributions are welcome.

- Fork the repository  
- Create feature branches  
- Add tests and documentation  
- Submit pull requests  

All contributions must comply with the LGPL-3.0-or-later license.

---

## License

Copyright © 2025–2026  
Kris Kirby, KE4AHR  

Licensed under the GNU Lesser General Public License v3.0 or later.

SPDX identifier:

    LGPL-3.0-or-later

