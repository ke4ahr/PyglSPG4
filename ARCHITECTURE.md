# PySGP4 Architecture

**Project Name:** PySGP4  
**Purpose:** High-performance, thread-safe, parallel implementation of the Simplified General Perturbations–4 (SGP4) satellite orbit propagation model  
**Language:** Python 3.10+  
**License:** GNU Lesser General Public License v3.0 (LGPL-3.0)  
**Domain:** Orbital mechanics, satellite tracking, space situational awareness  

---

## 1. Overview

PySGP4 is a clean-room, LGPL-licensed implementation of the Simplified General Perturbations–4 (SGP4) algorithm for propagating Earth-orbiting satellites from Two-Line Element (TLE) sets.

The architecture explicitly supports dual execution paths:

- Pure (native) Python, with zero third-party dependencies  
- NumPy-accelerated execution, enabling vectorization and SIMD acceleration  

while preserving:

- Determinism  
- Thread safety  
- Parallel scalability  
- Numerical fidelity to the reference SGP4 model  

This design makes PySGP4 suitable for ground-station software, space situational awareness systems, scientific simulation frameworks, and large-scale satellite catalog propagation.

---

## 2. Design Goals

### 2.1 Functional Goals

- Parse and validate TLEs  
- Initialize SGP4 orbital elements  
- Propagate position and velocity at arbitrary epochs  
- Support near-Earth and deep-space orbits  
- Match reference SGP4 outputs within accepted tolerances  

### 2.2 Non-Functional Goals

- Thread-safe propagation  
- Parallel batch execution  
- No global mutable state  
- Deterministic floating-point behavior  
- LGPL-compliant library usage  

### 2.3 Execution Flexibility

- Support pure Python execution with no external dependencies  
- Support NumPy-accelerated execution where applicable  
- Allow runtime backend selection  
- Guarantee numerical equivalence across backends within tolerance  

---

## 3. High-Level Architecture

    +-------------------+
    |  Public API       |
    |------------------|
    | propagate()       |
    | batch()           |
    +---------+---------+
              |
    +---------v---------+
    | Propagation Core  |
    |------------------|
    | Mean Elements     |
    | Perturbations     |
    | Kepler Solver     |
    +---------+---------+
              |
    +---------v---------+
    | Backend Abstraction|
    |------------------|
    | Python Backend    |
    | NumPy Backend     |
    +---------+---------+
              |
    +---------v---------+
    | Parallel Runtime  |
    |------------------|
    | Threads           |
    | Processes         |
    | Vectorization     |
    +-------------------+

---

## 4. Module Layout

    pysg4/
    ├── api/
    │   ├── propagate.py
    │   ├── batch.py
    │   └── exceptions.py
    │
    ├── tle/
    │   ├── parser.py
    │   ├── validator.py
    │   └── model.py
    │
    ├── sgp4/
    │   ├── initializer.py
    │   ├── near_earth.py
    │   ├── deep_space.py
    │   ├── perturbations.py
    │   ├── kepler.py
    │   └── state.py
    │
    ├── backend/
    │   ├── base.py
    │   ├── python.py
    │   ├── numpy.py
    │   └── selector.py
    │
    ├── math/
    │   ├── vectors.py
    │   ├── rotations.py
    │   ├── polynomials.py
    │   └── numerics.py
    │
    ├── time/
    │   ├── epochs.py
    │   ├── julian.py
    │   └── gmst.py
    │
    ├── parallel/
    │   ├── executor.py
    │   ├── strategies.py
    │   └── chunking.py
    │
    ├── constants.py
    ├── types.py
    └── __init__.py

---

## 5. Data Model

### 5.1 Immutable State Objects

All propagation inputs are represented as immutable dataclasses.

    @dataclass(frozen=True)
    class SGP4State:
        mean_motion: float
        eccentricity: float
        inclination: float
        argument_of_perigee: float
        right_ascension: float
        mean_anomaly: float
        drag_term: float

Benefits:

- Thread-safe by construction  
- Safe to share across threads and processes  
- Enables caching and memoization  
- Deterministic behavior  

---

## 6. Backend Abstraction Layer

### 6.1 Backend Interface

All numerical operations are routed through a backend interface.

    class MathBackend(Protocol):
        def sin(self, x): ...
        def cos(self, x): ...
        def sqrt(self, x): ...
        def atan2(self, y, x): ...
        def dot(self, a, b): ...
        def norm(self, v): ...

Backend characteristics:

- Stateless  
- Reentrant  
- Thread-safe  
- No hidden caches or side effects  

---

### 6.2 Native Python Backend

Module: backend/python.py

- Uses math and built-in types  
- Zero external dependencies  
- Default backend  
- Ideal for minimal or embedded environments  

    import math

    class PythonBackend:
        sin = staticmethod(math.sin)
        cos = staticmethod(math.cos)
        sqrt = staticmethod(math.sqrt)

---

### 6.3 NumPy Backend

Module: backend/numpy.py

- Uses NumPy ufuncs  
- Supports scalar and vector inputs  
- Enables SIMD and batch acceleration  
- Explicit float64 usage  

    import numpy as np

    class NumPyBackend:
        sin = staticmethod(np.sin)
        cos = staticmethod(np.cos)
        sqrt = staticmethod(np.sqrt)

Constraints:

- No in-place mutation  
- No reliance on global NumPy state  
- Arrays treated as immutable inputs  

---

## 7. Backend Selection

### 7.1 Runtime Selection

    from pysg4.backend import select_backend

    backend = select_backend(prefer="numpy")

Selection order:

1. Explicit user request  
2. NumPy availability  
3. Fallback to Python backend  

---

### 7.2 Per-Call Override

    propagate(state, epoch, backend="python")
    batch(states, epochs, backend="numpy")

This supports mixed workloads, controlled benchmarking, and deterministic regression testing.

---

## 8. Thread Safety Strategy

- No global mutable state  
- All constants are read-only  
- Functional, side-effect-free propagation core  
- Immutable inputs and outputs  
- Safe concurrent execution across threads and processes  

---

## 9. Parallel Execution Model

### 9.1 Parallelism Granularity

| Level       | Parallelizable | Notes                       |
|------------|----------------|-----------------------------|
| Satellite  | Yes            | Primary axis                |
| Epoch      | Yes            | Batch propagation           |
| Equation   | No             | Sequential for stability    |

---

### 9.2 Execution Backends

| Mode        | Python Backend | NumPy Backend |
|------------|----------------|---------------|
| Threads    | Yes            | GIL-limited   |
| Processes  | Yes            | Yes           |
| Vectorized | No             | Yes           |

Guidance:

- Threads plus NumPy for medium workloads  
- Processes plus Python for massive catalogs  
- NumPy vectorization for epoch grids  

---

## 10. Vectorization Strategy (NumPy)

### 10.1 Vectorized Components

- Mean anomaly propagation  
- Trigonometric perturbations  
- Coordinate transformations  
- Masked Kepler solver iterations  

### 10.2 Scalar-Only Components

- Deep-space branching logic  
- Convergence fallback paths  
- Error handling  

---

## 11. Numerical Determinism

| Scenario            | Guarantee               |
|---------------------|-------------------------|
| Same backend        | Bitwise repeatable      |
| Python vs NumPy     | Numerically equivalent  |
| Serial vs parallel  | Identical results       |

Mechanisms:

- Fixed iteration counts  
- Explicit convergence thresholds  
- Stable math order  
- Explicit sorting before batching  

---

## 12. Error Handling

### 12.1 Error Categories

| Error              | Description                |
|-------------------|----------------------------|
| TLEError          | Invalid TLE                |
| PropagationError  | Numerical failure          |
| ConvergenceError  | Kepler solver failure      |

Errors are raised immediately with no silent correction.

---

## 13. Validation and Testing

### 13.1 Reference Validation

- NASA and Vallado SGP4 test vectors  
- Cross-backend comparisons  

    assert pv_python.almost_equals(pv_numpy, tol=1e-12)

### 13.2 Test Layers

- Unit tests for math primitives  
- Integration tests for full propagation  
- Regression tests using catalog snapshots  

---

## 14. Performance Targets

| Scenario        | Backend              | Target     |
|-----------------|----------------------|------------|
| Single satellite| Python               | < 70 µs    |
| 1k satellites  | NumPy                | < 40 ms    |
| 10k satellites | NumPy + processes    | < 300 ms   |

---

## 15. LGPL-3.0 Licensing Considerations

- PySGP4 is a dynamically linkable LGPL library  
- NumPy is an optional dependency  
- Applications may remain proprietary  
- Modifications to PySGP4 must be released under LGPL  
- Backend abstraction prevents license contamination  

---

## 16. Future Extensions

- Full SDP4 deep-space refinements  
- Earth orientation parameters  
- GPU offload using CUDA or OpenCL  
- Kalman filtering and orbit determination integration  
- Real-time TLE ingestion pipelines  

---

## 17. Non-Goals

- Visualization  
- GUI or UI  
- Network-based TLE fetching  
- Orbit determination  

---

## 18. Summary

PySGP4 is architected as a pure, deterministic SGP4 implementation with dual Python and NumPy backends, full thread safety, parallel scalability, and LGPL-3.0–compliant linkage. The design scales from single-satellite ground stations to high-throughput catalog propagation systems without sacrificing correctness, reproducibility, or licensing flexibility.

