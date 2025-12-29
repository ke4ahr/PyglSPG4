# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Example: SatNOGS export for ISS passes

from pyglspg4.export.satnogs import export_satnogs_observations
from pyglspg4.groundstation.pass_prediction import predict_passes

# passes assumed computed already
export_satnogs_observations(
    passes=passes,
    satellite_id=25544,
    downlink_frequency_hz=145_800_000,
    path="iss_satnogs.json",
)

