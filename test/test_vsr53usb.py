from __future__ import annotations

import pytest

from vsr53.sys import dev_tty
from vsr53.vsr53dl import VSR53USB


@pytest.fixture()
def vacuum_sensor():
    sensor_address = 1
    vacuum_sense = VSR53USB(dev_tty, sensor_address)
    vacuum_sense.open_communication()
    yield vacuum_sense
    vacuum_sense.close_communication()


def test_device_query(vacuum_sensor):
    vacuum_sense = vacuum_sensor

    assert vacuum_sense.get_device_type() == "VSR213"
    assert vacuum_sense.get_product_name() == "VSR53USB"
    assert vacuum_sense.get_serial_number_device() == "22002816"
    assert vacuum_sense.get_serial_number_head() == "22002816"
    assert vacuum_sense.get_device_version() == 2.0
    assert vacuum_sense.get_firmware_version() == "0003"
