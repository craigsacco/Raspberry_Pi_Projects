#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(1, 'Libraries')
sys.path.insert(1, 'Libraries/Adafruit_Python_PureIO')
sys.path.insert(1, 'Libraries/Adafruit_Python_GPIO')

import time
from DS1624 import DS1624
from MAX127 import MAX127
from LM35OnMAX127 import LM35OnMAX127
from HIH3610OnMAX127 import HIH3610OnMAX127


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
