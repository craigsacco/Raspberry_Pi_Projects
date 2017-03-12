# -*- coding: utf-8 -*-

import Adafruit_GPIO.I2C as I2C


class DS1624(object):

    CMD_READ_TEMPERATURE = 0xAA
    CMD_START_CONVERSION = 0xEE
    CMD_STOP_CONVERSION = 0x22
    CMD_ACCESS_MEMORY = 0x17
    CMD_ACCESS_CONFIG = 0xAC

    CONVERSION_FACTOR = (1.0 / 256)

    def __init__(self, i2c=None, i2c_busnum=None, i2c_address=0x48, **kwargs):
        if i2c_address not in range(0x48, 0x50):
            raise ValueError("DS1624 I2C address must be in the range [0x48..0x4F]")
        # Create I2C device.
        self.__name__ = "DS1624"
        self._i2c = i2c or I2C
        self._i2c_busnum = i2c_busnum or self._i2c.get_default_bus()
        self._i2c_address = i2c_address
        self._device = self._i2c.get_i2c_device(self._i2c_address, self._i2c_busnum, **kwargs)

    def start_conversions(self):
        self._device.writeRaw8(DS1624.CMD_START_CONVERSION)

    def stop_conversions(self):
        self._device.writeRaw8(DS1624.CMD_STOP_CONVERSION)

    def get_data(self):
        value = self._device.readS16BE(DS1624.CMD_READ_TEMPERATURE)
        temperature = value * DS1624.CONVERSION_FACTOR
        return { "value": value, "temperature": temperature,
                 "temperature_uom": u"°C" }

    def get_temperature_raw(self):
        return self.get_data()["value"]

    def get_temperature(self):
        return self.get_data()["temperature"]

