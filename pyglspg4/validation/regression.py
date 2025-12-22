# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is part of Pyglspg4.

"""
Regression test scaffolding.
"""

from __future__ import annotations


class RegressionStore:
    """
    Simple in-memory regression store.

    Intended to be replaced by file-backed storage in CI.
    """

    def __init__(self):
        self._data = {}

    def record(self, key, value):
        self._data[key] = value

    def assert_same(self, key, value):
        if key not in self._data:
            raise KeyError("No regression baseline for key")
        if self._data[key] != value:
            raise AssertionError("Regression mismatch")

