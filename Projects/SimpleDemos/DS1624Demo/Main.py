#!/usr/bin/python
# -*- coding: utf-8 -*-

# import libraries from git submodules
import sys
sys.path.insert(1, '../../Drivers')
sys.path.insert(1, '../../Libraries/Adafruit_Python_PureIO')
sys.path.insert(1, '../../Libraries/Adafruit_Python_GPIO')

import time
from DS1624 import DS1624


def main():
    sensor = DS1624(address=0x48)
    sensor.start_conversions()
    try:
        while True:
            time.sleep(1)
            print "Temperature: {0:.3f}C".format(sensor.get_temperature())
    except KeyboardInterrupt:
        pass
    finally:
        sensor.stop_conversions()
        return 0


if __name__ == "__main__":
    sys.exit(main())
