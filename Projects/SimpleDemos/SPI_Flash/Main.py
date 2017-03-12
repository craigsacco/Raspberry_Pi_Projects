#!/usr/bin/python
# -*- coding: utf-8 -*-

# import libraries from git submodules
import sys
sys.path.insert(1, '../../../Drivers')
sys.path.insert(1, '../../../Libraries/Adafruit_Python_GPIO')

from M25PX80 import M25PX80


def main():
    flash = M25PX80(spi_port=0, spi_device=1, spi_speed=500000, gpio_hold=24)

    print "identity information"
    print flash.read_identity()

    print "remove existing block protections"
    flash.set_block_protection(M25PX80.BP_MODE_NONE)
    flash.wait_for_idle()
    assert flash.get_status() == 0

    OFFSET = 0xF8  # test around a page/subsector boundary

    print "sector erase"
    flash.sector_erase(OFFSET)

    if len(sys.argv) > 1:
        args = sys.argv[1:]
    else:
        args = ["Hello", "World!!!"]

    offset = OFFSET
    for arg in args:
        print "writing to offset {0}: \"{1}\"".format(offset, arg)
        flash.write_memory(offset, [ord(c) for c in arg])
        offset += len(arg)

    offset = OFFSET
    for arg in args:
        print "reading from offset {0}".format(offset)
        string = flash.read_memory(offset, len(arg))
        print " * expected \"{0}\", got \"{1}\"".format(arg, string)
        offset += len(arg)

if __name__ == "__main__":
    sys.exit(main())
