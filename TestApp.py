import sys
sys.path.insert(1, 'Libraries')
sys.path.insert(1, 'Libraries/Adafruit_Python_PureIO')
sys.path.insert(1, 'Libraries/Adafruit_Python_GPIO')

import time
from DS1624 import DS1624


def main():
    # initialise devices
    ds1624 = DS1624(address=0x48)
    ds1624.start_conversions()
    # start polling
    try:
        while True:
            temperature = ds1624.get_temperature()
            print temperature
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    # shutdown devices
    ds1624.stop_conversions()
    # done
    return 0


if __name__ == "__main__":
    sys.exit(main())
