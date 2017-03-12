# -*- coding: utf-8 -*-

import Adafruit_GPIO.I2C as I2C
import AdafruitOverrides


class MAX127(object):

    CTL_START = 0x80
    CTL_SELx_SHIFT = 4
    CTL_RANGE = 0x08
    CTL_BIPOLAR = 0x04
    CTL_OP_NORMAL = 0x00
    CTL_OP_POWERDOWN_STANDBY = 0x02
    CTL_OP_POWERDOWN_FULL = 0x03

    ADC_MAX_VALUE = 4095
    ADC_REFERENCE = 5.0

    def __init__(self, i2c=None, i2c_busnum=None, i2c_address=0x28, **kwargs):
        if i2c_address not in range(0x28, 0x30):
            raise ValueError("MAX127 I2C address must be in the range [0x28..0x2F]")
        # Create I2C device.
        self.__name__ = "MAX127"
        self._i2c = i2c or I2C
        self._i2c_busnum = i2c_busnum or self._i2c.get_default_bus()
        self._i2c_address = i2c_address
        self._device = self._i2c.get_i2c_device(self._i2c_address, self._i2c_busnum, **kwargs)

    def send_control_byte(self, value):
        self._device.writeRaw8(MAX127.CTL_START | value)

    def stand_by(self):
        self.send_control_byte(MAX127.CTL_OP_POWERDOWN_STANDBY)

    def power_down(self):
        self.send_control_byte(MAX127.CTL_OP_POWERDOWN_FULL)

    def start_conversion(self, channel, range=False, bipolar=False):
        byte = (channel << MAX127.CTL_SELx_SHIFT) | MAX127.CTL_OP_NORMAL
        if range:
            byte |= MAX127.CTL_RANGE
        if bipolar:
            byte |= MAX127.CTL_BIPOLAR
        self._channel = channel
        self._range = range
        self._bipolar = bipolar
        self.send_control_byte(byte)

    def get_data(self):
        value = 0
        if self._bipolar:
            value = (self._device.readRawS16BE() >> 4)
        else:
            value = (self._device.readRawU16BE() >> 4)
        voltage = (value * MAX127.ADC_REFERENCE) / \
                  (MAX127.ADC_MAX_VALUE >> (1 if self._bipolar else 0))
        if self._range:
            voltage = (voltage * 2.0)
        return { "value": value, "voltage": voltage,
                 "channel": self._channel, "range": self._range,
                 "bipolar": self._bipolar }

    def get_value(self):
        return self.get_data()["value"]

    def get_voltage(self):
        return self.get_data()["voltage"]