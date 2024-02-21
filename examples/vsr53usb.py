from __future__ import annotations

import logging

from vsr53 import VSR53USB
from vsr53.logger import log

if __name__ == "__main__":
    from vsr53.sys import dev_tty

    log.setLevel(logging.INFO)
    sensor_address = 1

    with VSR53USB(dev_tty, sensor_address) as vacuum_sense:
        vacuum_sense.get_device_type()
        vacuum_sense.get_product_name()
        vacuum_sense.get_serial_number_device()
        vacuum_sense.get_serial_number_head()
        vacuum_sense.get_device_version()
        vacuum_sense.get_firmware_version()
        vacuum_sense.get_measurement_value()
        vacuum_sense.get_measurement_value_piezo()
        vacuum_sense.get_measurement_value_pirani()
