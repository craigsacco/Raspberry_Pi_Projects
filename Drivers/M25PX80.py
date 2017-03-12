# -*- coding: utf-8 -*-

import Adafruit_GPIO.SPI as SPI
import Adafruit_GPIO.GPIO as GPIO


class M25PX80(object):

    CMD_READ_IDENTIFICATION = 0x9F
    CMD_READ_STATUS = 0x05
    CMD_WRITE_STATUS = 0x01
    CMD_WRITE_ENABLE = 0x06
    CMD_WRITE_DISABLE = 0x04
    CMD_ERASE_SUBSECTOR = 0x20
    CMD_ERASE_SECTOR = 0xD8
    CMD_ERASE_BULK = 0xC7
    CMD_READ_BYTES = 0x03
    CMD_PAGE_PROGRAM = 0x02

    STATUS_WIP = 0x01  # write-in-progress
    STATUS_WEL = 0x02  # write-enable latch
    STATUS_BP0 = 0x04  # block protect 0
    STATUS_BP1 = 0x08  # block protect 1
    STATUS_BP2 = 0x10  # block protect 2
    STATUS_TB = 0x20  # block protect top/bottom select
    STATUS_SRWD = 0x80  # status register write protect
    STATUS_WRITE_MASK = STATUS_BP0 | STATUS_BP1 | STATUS_BP2 | STATUS_TB |\
                        STATUS_SRWD

    BP_MODE_NONE = 0x00
    BP_MODE_64KB = STATUS_BP0
    BP_MODE_128KB = STATUS_BP1
    BP_MODE_256KB = STATUS_BP0 | STATUS_BP1
    BP_MODE_512KB = STATUS_BP2
    BP_MODE_FULL = STATUS_BP0 | STATUS_BP1 | STATUS_BP2
    BP_MODES = [BP_MODE_NONE, BP_MODE_64KB, BP_MODE_128KB, BP_MODE_256KB,
                BP_MODE_512KB, BP_MODE_FULL]

    MEMORY_SIZE = 1048576
    SECTOR_COUNT = 16
    SECTOR_SIZE = 65536
    SUBSECTOR_COUNT = 256
    SUBSECTOR_SIZE = 4096

    def __init__(self, spi=None, spi_port=0, spi_device=0, spi_speed=75000000,
                 gpio=None, gpio_hold=None, gpio_wp=None):
        # Create SPI device.
        self.__name__ = "M25PX80"
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

    def read_identity(self):
        out = [M25PX80.CMD_READ_IDENTIFICATION]
        result = list(self._device.transfer_half_duplex(out, 20))
        return {
            "manufacturer": result[0],
            "type": result[1],
            "capacity": result[2],
            "cfd_length": result[3],
            "cfd_data": result[4:]
        }

    def get_status(self):
        return list(self._device.transfer_half_duplex([M25PX80.CMD_READ_STATUS], 1))[0]

    def wait_for_idle(self):
        while (self.get_status() & M25PX80.STATUS_WIP) != 0:
            pass

    def bulk_erase(self, wait=True):
        self.set_write_enable(enable=True)
        self._device.write([M25PX80.CMD_ERASE_BULK])
        if wait:
            self.wait_for_idle()

    @staticmethod
    def serialise_offset(offset):
        return [(offset >> 16) & 0xff, (offset >> 8) & 0xff, offset & 0xff]

    def subsector_erase(self, offset, wait=True):
        self.set_write_enable(enable=True)
        self._device.write([M25PX80.CMD_ERASE_SUBSECTOR] + M25PX80.serialise_offset(offset))
        if wait:
            self.wait_for_idle()

    def sector_erase(self, offset, wait=True):
        self.set_write_enable(enable=True)
        self._device.write([M25PX80.CMD_ERASE_SECTOR] + M25PX80.serialise_offset(offset))
        if wait:
            self.wait_for_idle()

    def read_memory(self, offset, length):
        if offset < 0 or offset >= M25PX80.MEMORY_SIZE:
            raise ValueError("Offset is too large")
        out = [M25PX80.CMD_READ_BYTES] + M25PX80.serialise_offset(offset)
        return self._device.transfer_half_duplex(out, length)

    def write_page(self, offset, data, wait=True):
        if offset < 0 or offset >= M25PX80.MEMORY_SIZE:
            raise ValueError("Offset is too large")
        if (offset & 0xff) + len(data) > 256:
            raise ValueError("Write operation would overrun to the start of page")
        out = [M25PX80.CMD_PAGE_PROGRAM] + M25PX80.serialise_offset(offset) + data
        self.set_write_enable(enable=True)
        self._device.write(out)
        if wait:
            self.wait_for_idle()

    def write_memory(self, offset, data, wait=True):
        page_offset = offset
        page_remain = 256 - (offset & 0xff)
        data_offset = 0
        while True:
            chunk_length = min(page_remain, len(data) - data_offset)
            chunk_data = data[data_offset:data_offset+chunk_length]
            self.write_page(page_offset, chunk_data, wait)
            data_offset += chunk_length
            if data_offset == len(data):
                return
            # setup for next write operation - force waits between writes
            page_offset += chunk_length
            page_remain = 256
            if not wait:
                self.wait_for_idle()

    def set_block_protection(self, mode, top_or_bottom=False):
        if mode not in M25PX80.BP_MODES:
            raise ValueError("Block protection mode is not valid")
        status = mode | (M25PX80.STATUS_TB if top_or_bottom else 0)
        out = [M25PX80.CMD_WRITE_STATUS, status & M25PX80.STATUS_WRITE_MASK]
        self.set_write_enable(enable=True)
        self._device.write(out)

    def set_write_enable(self, enable=False):
        out = [M25PX80.CMD_WRITE_ENABLE if enable else M25PX80.CMD_WRITE_DISABLE]
        self._device.write(out)
