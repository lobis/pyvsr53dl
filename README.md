# vsr53

This is a Python library to communicate with Thyracont's VSR53USB pressure gauge.
It should also work with the VSR53DL model (over RS485) but I haven't tested it.

This library is a fork of [this repository](https://github.com/IFAEControl/pyvsr53dl).
All credits go to the original author.

The original library was designed for the RS485 protocol and does not work out of the box for the USB version of this
sensor, however, with some minor modifications such as allowing the user to set the baudrate and updating the default
value (to 9600 instead of 115200) it works perfectly.

I also updated the packaging to the latest standards and published it to PyPi.
