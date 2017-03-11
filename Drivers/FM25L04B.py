# -*- coding: utf-8 -*-

import Adafruit_GPIO.SPI as SPI
import Adafruit_GPIO.GPIO as GPIO


class FM25L04B(object):

    CMD_WRITE_ENABLE = 0x06
    CMD_WRITE_DISABLE = 0x04
    CMD_READ_STATUS = 0x05
    CMD_WRITE_STATUS = 0x01
    CMD_READ_MEMORY = 0x03
    CMD_WRITE_MEMORY = 0x02
    CMD_RWMEM_A8_BIT = 0x08

    STATUS_BP1 = 0x08
    STATUS_BP0 = 0x04
    STATUS_WEL = 0x02

    BP_MODE_NONE = 0x00
    BP_MODE_UPPER_QUARTER = STATUS_BP0
    BP_MODE_UPPER_HALF = STATUS_BP1
    BP_MODE_FULL = STATUS_BP0 + STATUS_BP1

    def __init__(self, spi=None, spi_port=0, spi_device=0, spi_speed=20000000,
                 gpio=None, gpio_hold=None, gpio_wp=None):
        # Create SPI device.
        self.__name__ = "FM25L04B"
        self._spi = spi or SPI
        self._device = self._spi.SpiDev(port=spi_port, device=spi_device,
                                        max_speed_hz=spi_speed)
        self._device.set_mode(SPI.MODE_CPOL0_CPHA0)
        self._device.set_bit_order(SPI.MSBFIRST)
        # Setup GPIO
        self._gpio = gpio or GPIO.get_platform_gpio()
        self._gpio_hold = gpio_hold
        self._gpio_wp = gpio_wp
        if self._gpio_hold is not None:
            self._gpio.setup(self._gpio_hold, GPIO.OUT)
            self.set_spi_hold(False)
        if self._gpio_wp is not None:
            self._gpio.setup(self._gpio_wp, GPIO.OUT)
            self.set_write_protection(False)

    def set_spi_hold(self, hold):
        if self._gpio_hold is None:
            raise NotImplementedError("Cannot adjust /HOLD line when not configured")
        self._gpio.output(self._gpio_hold, GPIO.LOW if hold else GPIO.HIGH)

    def set_write_protection(self, protect):
        if self._gpio_wp is None:
            raise NotImplementedError("Cannot adjust /WP line when not configured")
        self._gpio.output(self._gpio_wp, GPIO.LOW if protect else GPIO.HIGH)

    def half_duplex(self, out_data, in_len):
        in_data = self._device.transfer(bytearray([FM25L04B.CMD_READ_STATUS] + ([0x00] * in_len)))
        return in_data[len(out_data):]

    def get_status(self):
        in_data = self.half_duplex([FM25L04B.CMD_READ_STATUS], 1)
        return in_data[0]

    def read_memory(self, offset, data):
        pass

    def write_memory(self, offset, length):
        pass

    def set_block_protection(self, mode):
        pass

