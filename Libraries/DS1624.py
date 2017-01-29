import Adafruit_GPIO as GPIO
import Adafruit_GPIO.I2C as I2C

class DS1624(object):

    CMD_READ_TEMPERATURE = 0xAA
    CMD_START_CONVERSION = 0xEE
    CMD_STOP_CONVERSION = 0x22
    CMD_ACCESS_MEMORY = 0x17
    CMD_ACCESS_CONFIG = 0xAC

    CONVERSION_FACTOR = (1.0 / 256)

    def __init__(self, address=0x48, busnum=None, i2c=None, **kwargs):
        address = int(address)
        self.__name__ = \
            "DS1624" if address in range(0x48, 0x50) else \
            "Bad address for DS1624: 0x%02X not in range [0x48..0x4F]" % address
        if self.__name__[0] != 'D':
            raise ValueError(self.__name__)
        # Create I2C device.
        self._address = address
        self._i2c = i2c or I2C
        self._busnum = busnum or self._i2c.get_default_bus()
        self._device = self._i2c.get_i2c_device(self._address, self._busnum, **kwargs)

    def start_conversions(self):
        self._device.writeRaw8(DS1624.CMD_START_CONVERSION)

    def stop_conversions(self):
        self._device.writeRaw8(DS1624.CMD_STOP_CONVERSION)

    def get_temperature_raw(self):
        return self._device.readS16BE(DS1624.CMD_READ_TEMPERATURE)

    def get_temperature(self):
        value = self.get_temperature_raw()
        return value * DS1624.CONVERSION_FACTOR
