#!/usr/bin/python
# -*- coding: utf-8 -*-

# import libraries from git submodules
import sys
sys.path.insert(1, '../../../Drivers')
sys.path.insert(1, '../../../Libraries/Adafruit_Python_PureIO')
sys.path.insert(1, '../../../Libraries/Adafruit_Python_GPIO')

import time
from FM25L04B import FM25L04B


def main():
    fram = FM25L04B(spi_port=0, spi_device=0, gpio_hold=23)
    print fram.get_status()


if __name__ == "__main__":
    sys.exit(main())
