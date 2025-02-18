from __future__ import annotations

import re
from abc import ABC, abstractmethod

import serial
import serial.rs485

from vsr53 import ErrorMessages
from vsr53.AccessCodes import AccessCode as AC
from vsr53.Commands import Commands as CMD
from vsr53.DisplayModes import Orientation as Orientation
from vsr53.DisplayModes import Units as Units
from vsr53.logger import log
from vsr53.ThyrCommPackage import ThyrCommPackage


class VSR53(ABC):
    @abstractmethod
    def __init__(self):
        self._serial = None
        self._address = None

    def open_communication(self):
        opening_port_trials = 0
        if self._serial.isOpen():
            self._serial.flush()
            log.info("Port is Open!")
        elif not self._serial.isOpen() and opening_port_trials < 5:
            log.info("Port closed, trying to open...")
            self._serial.open()
            opening_port_trials += 1
            self.open_communication()

    def close_communication(self):
        """
        Closes communication with serial device
        :return: None
        """
        self._serial.flush()
        self._serial.close()
        log.info("Closing communication with device")

    def __enter__(self):
        self.open_communication()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_communication()

    def get_device_type(self):
        """
        Query of device type, e.g. VSR205
        :return: device_type
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Type_Device
        device_type = self._read_data_transaction(pack)
        log.info(f"Device type: {device_type}")
        return device_type

    def get_product_name(self):
        """
        Query of product name (article number)
        :return: product_name
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Product_Name
        product_name = self._read_data_transaction(pack)
        log.info(f"Product name: {product_name}")
        return product_name

    def get_serial_number_device(self):
        """
        Query of device serial number
        :return: device_serial_number
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Serial_Number_Device
        device_serial_number = self._read_data_transaction(pack)
        log.info(f"Device serial number: {device_serial_number}")
        return device_serial_number

    def get_serial_number_head(self):
        """
        Query of sensor head serial number
        :return: sensor_head_serial_number
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Serial_Number_Head
        sensor_head_serial_number = self._read_data_transaction(pack)
        log.info(f"Head serial number: {sensor_head_serial_number}")
        return sensor_head_serial_number

    def get_device_version(self):
        """
        Query of the device’s hardware version
        :return: device_version
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Version_Device
        device_version = float(self._read_data_transaction(pack))
        log.info(f"Device version: {device_version}")
        return device_version

    def get_firmware_version(self):
        """
        Query of the device’s firmware version
        :return: firmware_version
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Version_Firmware
        firmware_version = self._read_data_transaction(pack)
        log.info(f"Firmware version: {firmware_version}")
        return firmware_version

    def get_bootloader_version(self):
        """
        Query of the device’s bootloader version
        :return: bootloader_version
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Version_Bootloader
        bootloader_version = float(self._read_data_transaction(pack))
        log.info(f"Bootloader version: {bootloader_version}")
        return bootloader_version

    def set_baud_rate(self, baud_rate):
        """
        Set the baud rate for data transmission
        :param baud_rate: Value possibilities: 9600, 14400, 19200, 28800, 38400, 57600, 115200 Bd
        :return:None
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Baud_Rate
        pack.data = baud_rate
        log.info(f"Setting baud rate to {baud_rate}")
        self._write_data_transaction(pack)

    def get_response_delay(self):
        """
        Query the time delay between receiving a telegram and sending the answer.
        Value range: 1 ... 99999 μs (default 5500 μs)
        :return: response_delay
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Response_Delay
        response_delay = float(self._read_data_transaction(pack))
        log.info(f"Response delay: {response_delay}")
        return response_delay

    def set_response_delay(self, response_delay):
        """
        Set the time delay between receiving a telegram and sending the answer.
        :param response_delay: Value range: 1 ... 99999 μs (default 5500 μs)
        :return:
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Response_Delay
        pack.data = response_delay
        log.info(f"Setting response delay to: {response_delay}")
        self._write_data_transaction(pack)

    def get_display_unit(self):
        """
        Query the display unit in the device's display
        :return: display_unit
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Display_Unit
        display_unit = self._read_data_transaction(pack)
        log.info(f"Display units: {display_unit}")
        return display_unit

    def set_display_unit(self, display_unit):
        """
        Set the display unit in the device's display
        :param display_unit: Selectable amongst :Units.MBAR, Units.TORR and Units.HPA
        :return:
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Display_Unit
        pack.data = display_unit
        log.info(f"Setting display units to: {display_unit}")
        self._write_data_transaction(pack)

    def get_display_orientation(self):
        """
        Get the display orientation of the device NORMAL or ROTATED
        :return: display_orientation
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Display_Orientation
        display_orientation = self._read_data_transaction(pack)
        display_orientation_name = "NORMAL"
        if int(display_orientation) != int(Orientation.NORMAL):
            display_orientation_name = "ROTATED"
        log.info(f"Display orientation: {display_orientation_name}")
        return display_orientation

    def set_display_orientation(self, display_orientation):
        """
        Set the display orientation of the device NORMAL or ROTATED
        :param display_orientation: Selectable amongst Orientation.NORMAL and Orientation.ROTATED
        :return:
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Display_Orientation
        pack.data = display_orientation
        log.info(f"Setting display orientation to {display_orientation}")
        self._write_data_transaction(pack)

    def get_operating_hours(self):
        """
        Query the device's operating hours
        :return: operating_hours
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Operating_Hours
        operating_hours = float(self._read_data_transaction(pack)) / 4.0
        log.info(f"Device's been operating for {operating_hours}h")
        return operating_hours

    def get_measurement_range(self):
        """
        Query measurement range of the gauge
        :return: measurement_range_lo, measurement_range_hi
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Measurement_Range
        data = self._read_data_transaction(pack)
        measurement_range_lo = float(data[1:6])
        measurement_range_hi = float(data[7:11])
        log.info(
            f"Measurement range is: {measurement_range_lo, measurement_range_hi} {Units.MBAR}"
        )
        return measurement_range_lo, measurement_range_hi

    def get_measurement_value(self):
        """
        Query current pressure measurement
        :return: pressure_measurement
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Measurement_Value
        pressure_measurement = float(self._read_data_transaction(pack))
        log.info(f"Measurement is: {pressure_measurement} {Units.MBAR}")
        return pressure_measurement

    def get_measurement_value_pirani(self):
        """
        Query current pressure measurement of the Pirani sensor
        :return: pressure_measurement
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Measurement_Value_1
        pressure_measurement = float(self._read_data_transaction(pack))
        log.info(f"Measurement with pirani is: {pressure_measurement} {Units.MBAR}")
        return pressure_measurement

    def get_measurement_value_piezo(self):
        """
        Query current pressure measurement of the Piezo sensor
        :return: pressure_measurement
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Measurement_Value_2
        pressure_measurement = float(self._read_data_transaction(pack))
        log.info(f"Measurement with piezo is: {pressure_measurement} {Units.MBAR}")
        return pressure_measurement

    def get_relay_1_status(self):
        """
        Get Relay 1 Status
        :return: relay_1_status
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Relay_1
        relay_1_status = self._read_data_transaction(pack)
        pattern1 = "T(.*?)F"
        t_value = float(re.search(pattern1, relay_1_status).group(1))
        f_value = float(str(relay_1_status).split("F", 1)[1])
        log.info(f"Relay 1 status: T{t_value} and F{f_value}")
        return t_value, f_value

    def get_relay_2_status(self):
        """
        Get Relay 2 Status
        :return: relay_2_status
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Relay_2
        relay_2_status = self._read_data_transaction(pack)
        pattern1 = "T(.*?)F"
        t_value = float(re.search(pattern1, relay_2_status).group(1))
        f_value = float(str(relay_2_status).split("F", 1)[1])
        log.info(f"Relay 2 status: T{t_value} and F{f_value}")
        return t_value, f_value

    def set_relay_1_status(self, relay_status):
        """
        Set Relay 1 Status
        :return: relay_1_status
        :param relay_status: Not defined in discrete values yet, a string with the appropriate format has to used
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Relay_1
        pack.relay_status = relay_status
        log.info(f"Setting Relay 1 status: {relay_status}")
        self._write_data_transaction(pack)

    def set_relay_2_status(self, relay_status):
        """
        Set Relay 2 Status
        :return: relay_2_status
        :param relay_status: Not defined in discrete values yet, a string with the appropriate format has to used
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Relay_2
        pack.relay_status = relay_status
        log.info(f"Setting Relay 2 status: {relay_status}")
        self._write_data_transaction(pack)

    def restart_device(self):
        """
        Makes device restart
        :return: None
        """
        pack = ThyrCommPackage(self._address)
        pack.cmd = CMD.Device_Restart
        pack.data = 0
        log.info("Restarting device")
        self._write_data_transaction(pack)

    def _read_data_transaction(self, pack):
        pack.data = 0
        pack.access_code = AC.RD_TX
        self._instruction_exchange(pack)
        return pack.data

    def _write_data_transaction(self, pack):
        pack.access_code = AC.WR_TX
        return self._instruction_exchange(pack)

    def _instruction_exchange(self, pack):
        fine_transaction = False
        message = b""
        while not fine_transaction:
            self._send_message(pack)
            message = self._receive_message()
            if message != b"" and message[-1] == 13 and len(message) < 30:
                fine_transaction = True
            else:
                log.error("BAD TRANSACTION")
                fine_transaction = False
                self._serial.flush()
        pack.parse_answer(message)
        if pack.access_code == AC.ERR_RX:
            log.error(f"{ErrorMessages.MSG[pack.data]}")
        return message

    def _send_message(self, pack):
        log.debug(f"TXin' this: {pack.get_string()}")
        self._serial.write(pack.get_package_ascii_list())

    def _receive_message(self):
        message = self._serial.readline()
        log.debug(f"RXin' this: {message}")
        return message


class VSR53DL(VSR53):
    """
    Thyracont's VSR53DL vacuum sensor RS458 interface
    """

    def __init__(self, port: str, *, address: int = 1, baudrate: int = 9600):
        """
        Constructor will initiate serial port communication in rs485 mode and define address for device.
        :param port: device label assigned by the operating system when the device is connected
        :param address: Defined by the address switch mounted in the device from 1 to 16
        :param baudrate: Baud rate for data transmission
        """
        self._serial = serial.rs485.RS485()
        self._serial.port = port
        self._serial.baudrate = baudrate
        self._serial.parity = serial.PARITY_NONE
        self._serial.stopbits = serial.STOPBITS_ONE
        self._serial.bytesize = serial.EIGHTBITS
        self._serial.timeout = 0.02
        self._serial.rs485_mode = serial.rs485.RS485Settings()

        self._address = address


class VSR53USB(VSR53):
    def __init__(self, port: str, *, address: int = 1, baudrate: int = 9600):
        self._serial = serial.Serial()
        self._serial.port = port
        self._serial.baudrate = baudrate
        self._serial.parity = serial.PARITY_NONE
        self._serial.stopbits = serial.STOPBITS_ONE
        self._serial.bytesize = serial.EIGHTBITS
        self._serial.timeout = 0.02

        self._address = address
