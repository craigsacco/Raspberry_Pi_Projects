# -*- coding: utf-8 -*-

import Adafruit_GPIO.I2C as I2C
import Adafruit_GPIO.GPIO as GPIO


class EE24LC256(object):

    MEMORY_SIZE = 32768

    def __init__(self, i2c=None, i2c_busnum=None, i2c_address=0x50,
                 gpio=None, gpio_wp=None, **kwargs):
        if i2c_address not in range(0x50, 0x57):
            raise ValueError("24LC256 I2C address must be in the range [0x50..0x57]")
        # Create I2C device.
        self.__name__ = "24LC256"
        self._i2c = i2c or I2C
        self._i2c_busnum = i2c_busnum or self._i2c.get_default_bus()
        self._i2c_address = i2c_address
        self._device = self._i2c.get_i2c_device(self._i2c_address, self._i2c_busnum, **kwargs)
        # Setup GPIO
        self._gpio = gpio or GPIO.get_platform_gpio()
        self._gpio_wp = gpio_wp
        if self._gpio_wp is not None:
            self._gpio.setup(self._gpio_wp, GPIO.OUT)
            self.set_write_protection(False)

    def set_write_protection(self, protect):
        if self._gpio_wp is None:
            raise NotImplementedError("Cannot adjust WP line when not configured")
        self._gpio.output(self._gpio_wp, GPIO.HIGH if protect else GPIO.LOW)

    def read_memory(self, offset, length):
        if offset < 0 or offset >= EE24LC256.MEMORY_SIZE:
            raise ValueError("Offset is too large")
        # TODO: update the GPIO/PureIO modules to use a bulk transaction using ioctl instead of fnctl
        out = [(offset >> 8) & 0xff, offset & 0xff]
        self._device.writeBytes(out)
        return bytearray(self._device.readBytes(length))

    def write_memory(self, offset, data):
        if offset < 0 or offset >= EE24LC256.MEMORY_SIZE:
            raise ValueError("Offset is too large")
        out = [(offset >> 8) & 0xff, offset & 0xff] + data
        self._device.writeBytes(out)
