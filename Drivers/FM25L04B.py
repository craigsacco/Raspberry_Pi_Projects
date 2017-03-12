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
    BP_MODES = [BP_MODE_NONE, BP_MODE_UPPER_QUARTER, BP_MODE_UPPER_HALF,
                BP_MODE_FULL]

    MEMORY_SIZE = 512

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
        self._gpio.output(self._gpio_hold, GPIO.LOW if hold else GPIO.HIGH)  # active-low

    def set_write_protection(self, protect):
        if self._gpio_wp is None:
            raise NotImplementedError("Cannot adjust /WP line when not configured")
        self._gpio.output(self._gpio_wp, GPIO.LOW if protect else GPIO.HIGH)  # active-low

    def get_status(self):
        data = self._device.transfer_half_duplex([FM25L04B.CMD_READ_STATUS], 1)
        return data[0]

    def read_memory(self, offset, length):
        if offset < 0 or offset >= FM25L04B.MEMORY_SIZE:
            raise ValueError("Offset is too large")
        out = [FM25L04B.CMD_READ_MEMORY | (FM25L04B.CMD_RWMEM_A8_BIT if offset > 0xFF else 0),
               offset & 0xFF]
        return self._device.transfer_half_duplex(out, length)

    def write_memory(self, offset, data):
        if offset < 0 or offset >= FM25L04B.MEMORY_SIZE:
            raise ValueError("Offset is too large")
        out = [FM25L04B.CMD_WRITE_MEMORY | (FM25L04B.CMD_RWMEM_A8_BIT if offset > 0xFF else 0),
               offset & 0xFF] + data
        self._device.write(out)

    def set_block_protection(self, mode):
        if mode not in FM25L04B.BP_MODES:
            raise ValueError("Block protection mode is not valid")
        out = [FM25L04B.CMD_WRITE_STATUS,
               mode & (FM25L04B.STATUS_BP0 | FM25L04B.STATUS_BP1)]
        self._device.write(out)

    def set_write_enable(self, enable):
        out = [FM25L04B.CMD_WRITE_ENABLE if enable
               else FM25L04B.CMD_WRITE_DISABLE]
        self._device.write(out)
