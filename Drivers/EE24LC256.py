# -*- coding: utf-8 -*-

import Adafruit_GPIO.I2C as I2C


class EE24LC256(object):

    MEMORY_SIZE = 32768

    def __init__(self, i2c=None, i2c_busnum=None, i2c_address=0x50, **kwargs):
        if i2c_address not in range(0x50, 0x57):
            raise ValueError("24LC256 I2C address must be in the range [0x50..0x57]")
        # Create I2C device.
        self.__name__ = "24LC256"
        self._i2c = i2c or I2C
        self._i2c_busnum = i2c_busnum or self._i2c.get_default_bus()
        self._i2c_address = i2c_address
        self._device = self._i2c.get_i2c_device(self._i2c_address, self._i2c_busnum, **kwargs)

    def read_memory(self, offset, length):
        if offset < 0 or offset >= EE24LC256.MEMORY_SIZE:
            raise ValueError("Offset is too large")
        out = [(offset >> 8) & 0xff, offset & 0xff]
        self._device.writeBytes(out)
        return bytearray(self._device.readBytes(length))

    def write_memory(self, offset, data):
        if offset < 0 or offset >= EE24LC256.MEMORY_SIZE:
            raise ValueError("Offset is too large")
        out = [(offset >> 8) & 0xff, offset & 0xff] + data
        self._device.writeBytes(out)

