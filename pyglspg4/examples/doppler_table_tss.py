# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Example: Doppler frequency table for ISS pass

from pyglspg4.export.frequency_tables import generate_frequency_table
from pyglspg4.export.frequency_tables import export_csv

# Example inputs
downlink_hz = 145_800_000
relative_velocities_mps = [
    -7500, -5000, -2500, 0, 2500, 5000, 7500
]

table = generate_frequency_table(
    nominal_frequency_hz=downlink_hz,
    relative_velocity_mps=relative_velocities_mps,
)

export_csv(table, "iss_doppler.csv")

