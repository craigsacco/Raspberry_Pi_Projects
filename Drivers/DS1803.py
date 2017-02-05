# -*- coding: utf-8 -*-

import Adafruit_GPIO.I2C as I2C


class DS1803(object):

    CMD_WRITE_POT0 = 0xA9
    CMD_WRITE_POT1 = 0xAA
    CMD_WRITE_BOTH_POTS = 0xAF

    VARIANT_10K = 10000
    VARIANT_50K = 50000
    VARIANT_100K = 100000
    VARIANTS = [VARIANT_10K, VARIANT_50K, VARIANT_100K]

    def __init__(self, address=0x28, variant=VARIANT_10K,
                 busnum=None, i2c=None, **kwargs):
        address = int(address)
        self.__name__ = \
            "DS1803" if address in range(0x28, 0x30) else \
            "Bad address for DS1803: 0x%02X not in range [0x28..0x2F]" % address
        self.__name__ = \
            "DS1803" if variant in DS1803.VARIANTS else \
            "Invalid variant: {0}".format(variant)
        if self.__name__[0] != 'D':
            raise ValueError(self.__name__)
        # Create I2C device.
        self._address = address
        self._variant = variant
        self._i2c = i2c or I2C
        self._busnum = busnum or self._i2c.get_default_bus()
        self._device = self._i2c.get_i2c_device(self._address, self._busnum, **kwargs)

    def send_command(self, command, value):
        self._device.write8(command, value)

    def resistance_to_value(self, resistance):
        if resistance > self._variant:
            raise ValueError("Resistance {0} is invalid".format(resistance))
        value = int((resistance * 256.0) / self._variant)
        if value >= 256:
            value = 255
        return value

    def set_pot0_resistance(self, resistance):
        self.send_command(DS1803.CMD_WRITE_POT0, self.resistance_to_value(resistance))

    def set_pot1_resistance(self, resistance):
        self.send_command(DS1803.CMD_WRITE_POT1, self.resistance_to_value(resistance))

    def set_both_pots_resistance(self, resistance):
        self.send_command(DS1803.CMD_WRITE_BOTH_POTS, self.resistance_to_value(resistance))
