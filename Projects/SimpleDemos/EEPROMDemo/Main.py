#!/usr/bin/python
# -*- coding: utf-8 -*-

# import libraries from git submodules
import sys
sys.path.insert(1, '../../../Drivers')
sys.path.insert(1, '../../../Libraries/Adafruit_Python_PureIO')
sys.path.insert(1, '../../../Libraries/Adafruit_Python_GPIO')

import time
from EE24LC256 import EE24LC256


def main():
    eeprom = EE24LC256(i2c_address=0x50)

    if len(sys.argv) > 1:
        args = sys.argv[1:]
    else:
        args = ["Hello", "World!!!"]

    offset = 0
    for arg in args:
        print "writing to offset {0}: \"{1}\"".format(offset, arg)
        eeprom.write_memory(offset, [ord(c) for c in arg])
        time.sleep(0.005)  # takes 5ms to write to EEPROM
        offset += len(arg)

    offset = 0
    for arg in args:
        print "reading from offset {0}".format(offset)
        string = eeprom.read_memory(offset, len(arg))
        print " * expected \"{0}\", got \"{1}\"".format(arg, string)
        offset += len(arg)

if __name__ == "__main__":
    sys.exit(main())
