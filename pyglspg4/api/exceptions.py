# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Exception hierarchy for Pyglspg4.
"""

class Pyglspg4Error(Exception):
    """Base exception for all Pyglspg4 errors."""


class TLEError(Pyglspg4Error):
    """Raised when a TLE is malformed or invalid."""


class PropagationError(Pyglspg4Error):
    """Raised when numerical propagation fails."""


class ConvergenceError(PropagationError):
    """Raised when an iterative solver fails to converge."""

