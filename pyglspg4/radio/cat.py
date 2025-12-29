# Copyright (C) 2025-2026 Kris Kirby, KE4AHR
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# CAT control via Hamlib / rigctl
#
# Provides a minimal, safe interface for sending
# frequency updates to radio transceivers during
# satellite passes.
#
# This module does not require Hamlib at import time.
# It executes rigctl as an external process when used.

from __future__ import annotations

import subprocess
from typing import Optional


class RigController:
    """
    CAT controller using rigctl (Hamlib).
    """

    def __init__(
        self,
        rigctl_path: str = "rigctl",
        rig_model: int = 2,
        rig_port: Optional[str] = None,
        rig_speed: Optional[int] = None,
    ) -> None:
        self.rigctl_path = rigctl_path
        self.rig_model = rig_model
        self.rig_port = rig_port
        self.rig_speed = rig_speed

    def _base_cmd(self) -> list[str]:
        cmd = [self.rigctl_path, "-m", str(self.rig_model)]
        if self.rig_port:
            cmd.extend(["-r", self.rig_port])
        if self.rig_speed:
            cmd.extend(["-s", str(self.rig_speed)])
        return cmd

    def set_frequency(self, frequency_hz: float) -> bool:
        """
        Set transceiver frequency.

        Parameters
        ----------
        frequency_hz : float
            Frequency in Hz

        Returns
        -------
        bool
            True if command succeeded
        """

        cmd = self._base_cmd()
        cmd.extend(["F", str(int(frequency_hz))])

        try:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except (OSError, subprocess.CalledProcessError):
            return False

    def set_mode(self, mode: str, width: Optional[int] = None) -> bool:
        """
        Set transceiver mode.

        Parameters
        ----------
        mode : str
            Mode string (e.g., FM, USB, LSB)
        width : int, optional
            Filter width (Hz)

        Returns
        -------
        bool
        """

        cmd = self._base_cmd()
        if width is not None:
            cmd.extend(["M", mode, str(width)])
        else:
            cmd.extend(["M", mode])

        try:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except (OSError, subprocess.CalledProcessError):
            return False

