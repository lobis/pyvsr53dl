from __future__ import annotations

import pytest

from vsr53.DisplayModes import Units
from vsr53.sys import dev_tty
from vsr53.vsr53 import VSR53DL


@pytest.fixture()
def vacuum_sensor():
    sensor_address = 1
    vacuum_sense = VSR53DL(dev_tty, sensor_address)
    vacuum_sense.open_communication()
    yield vacuum_sense
    vacuum_sense.close_communication()


def test_device_query(vacuum_sensor):
    vacuum_sense = vacuum_sensor

    assert vacuum_sense.get_device_type() == "VSR205"
    assert vacuum_sense.get_product_name() == "VSR53DL"
    assert vacuum_sense.get_serial_number_device() == "20002583"
    assert vacuum_sense.get_serial_number_head() == "20002583"
    assert vacuum_sense.get_device_version() == 2.0
    assert vacuum_sense.get_firmware_version() == "0215"
    assert vacuum_sense.get_bootloader_version() == 2.0

    vacuum_sense.set_display_unit(Units.MBAR)
    assert vacuum_sense.get_display_unit() == Units.MBAR
