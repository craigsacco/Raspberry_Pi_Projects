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
    fram = FM25L04B(spi_port=0, spi_device=0, spi_speed=500000, gpio_hold=23)

    # remove existing block protections and disable writes
    fram.set_write_enable(True)  # needs to be issued before any write
    fram.set_block_protection(FM25L04B.BP_MODE_NONE)
    fram.set_write_enable(False)
    assert fram.get_status() == 0

    if len(sys.argv) > 1:
        args = sys.argv[1:]
    else:
        args = ["Hello", "World!!!"]

    offset = 0
    for arg in args:
        print "writing to offset {0}: \"{1}\"".format(offset, arg)
        fram.set_write_enable(True)  # needs to be issued before any write
        fram.write_memory(offset, [ord(c) for c in arg])
        offset += len(arg)

    offset = 0
    for arg in args:
        print "reading from offset {0}".format(offset)
        string = fram.read_memory(offset, len(arg))
        print " * expected \"{0}\", got \"{1}\"".format(arg, string)
        offset += len(arg)

if __name__ == "__main__":
    sys.exit(main())
