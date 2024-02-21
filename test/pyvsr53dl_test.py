from __future__ import annotations

import logging
import unittest

from vsr53.DisplayModes import Units
from vsr53.logger import log
from vsr53.vsr53dl import VSR53DL


class TestVacuumSense(unittest.TestCase):

    def test_device_query(self):
        log.setLevel(logging.INFO)
        from vsr53.sys import dev_tty

        sensor_address = 1
        vacuum_sense = VSR53DL(dev_tty, sensor_address)
        vacuum_sense.open_communication()

        self.assertAlmostEqual(vacuum_sense.get_device_type(), "VSR205")
        self.assertAlmostEqual(vacuum_sense.get_product_name(), "VSR53DL")
        self.assertAlmostEqual(vacuum_sense.get_serial_number_device(), "20002583")
        self.assertAlmostEqual(vacuum_sense.get_serial_number_head(), "20002583")
        self.assertAlmostEqual(vacuum_sense.get_device_version(), 2.0)
        self.assertAlmostEqual(vacuum_sense.get_firmware_version(), "0215")
        self.assertAlmostEqual(vacuum_sense.get_bootloader_version(), 2.0)
        vacuum_sense.set_display_unit(Units.MBAR)
        self.assertAlmostEqual(vacuum_sense.get_display_unit(), Units.MBAR)

        vacuum_sense.close_communication()
