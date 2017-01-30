import sys
sys.path.insert(1, 'Libraries')
sys.path.insert(1, 'Libraries/Adafruit_Python_PureIO')
sys.path.insert(1, 'Libraries/Adafruit_Python_GPIO')

import time
from DS1624 import DS1624
from MAX127 import MAX127


class LM35OnMAX127(object):

    def __init__(self, adc, channel):
        self._adc = adc
        self._channel = channel

    def get_temperature(self):
        self._adc.start_conversion(channel=self._channel, bipolar=False)
        voltage = self._adc.get_voltage(bipolar=False)
        temperature = voltage * 100.0
        return temperature


def main():
    # initialise devices
    ds1624 = DS1624(address=0x48)
    ds1624.start_conversions()
    max127 = MAX127(address=0x28)
    lm35_1 = LM35OnMAX127(adc=max127, channel=0)
    lm35_2 = LM35OnMAX127(adc=max127, channel=1)
    # start polling
    try:
        while True:
            temperature1 = ds1624.get_temperature()
            temperature2 = lm35_1.get_temperature()
            temperature3 = lm35_2.get_temperature()
            print temperature1, temperature2, temperature3
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    # shutdown devices
    ds1624.stop_conversions()
    # done
    return 0


if __name__ == "__main__":
    sys.exit(main())
