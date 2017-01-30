import sys
sys.path.insert(1, 'Libraries')
sys.path.insert(1, 'Libraries/Adafruit_Python_PureIO')
sys.path.insert(1, 'Libraries/Adafruit_Python_GPIO')

import time
from DS1624 import DS1624
from MAX127 import MAX127


class LM35OnMAX127(object):

    OFFSET_V_0C = 0.0
    GAIN_VpC = 0.01

    def __init__(self, adc, channel):
        self._adc = adc
        self._channel = channel

    def get_temperature(self):
        self._adc.start_conversion(channel=self._channel, bipolar=False)
        voltage = self._adc.get_voltage(bipolar=False)
        temperature = (voltage - LM35OnMAX127.OFFSET_V_0C) /\
                      LM35OnMAX127.GAIN_VpC
        return temperature


class HIH3610OnMAX127(object):

    OFFSET_V_0RHpc = 0.958
    GAIN_VpRHpc = 0.03068

    def __init__(self, adc, channel):
        self._adc = adc
        self._channel = channel

    def get_humidity(self):
        self._adc.start_conversion(channel=self._channel, bipolar=False)
        voltage = self._adc.get_voltage(bipolar=False)
        humidity = (voltage - HIH3610OnMAX127.OFFSET_V_0RHpc) / \
                   HIH3610OnMAX127.GAIN_VpRHpc
        return humidity


def main():
    # initialise devices
    ds1624 = DS1624(address=0x48)
    ds1624.start_conversions()
    max127 = MAX127(address=0x28)
    lm35_1 = LM35OnMAX127(adc=max127, channel=0)
    lm35_2 = LM35OnMAX127(adc=max127, channel=1)
    hih3610 = HIH3610OnMAX127(adc=max127, channel=2)
    # start polling
    try:
        while True:
            temperature1 = ds1624.get_temperature()
            temperature2 = lm35_1.get_temperature()
            temperature3 = lm35_2.get_temperature()
            humidity = hih3610.get_humidity()
            print temperature1, temperature2, temperature3, humidity
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    # shutdown devices
    ds1624.stop_conversions()
    max127.power_down()
    # done
    return 0


if __name__ == "__main__":
    sys.exit(main())
