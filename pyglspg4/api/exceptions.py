# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Public exception types for Pyglspg4.

These exceptions define the stable error surface of the library and
are intended to be caught by user applications.
"""


class Pyglspg4Error(Exception):
    """
    Base class for all Pyglspg4 exceptions.
    """
    pass


class ConvergenceError(Pyglspg4Error):
    """
    Raised when a numerical solver fails to converge.
    """
    pass


class PropagationError(Pyglspg4Error):
    """
    Raised when orbit propagation cannot be completed.
    """
    pass

