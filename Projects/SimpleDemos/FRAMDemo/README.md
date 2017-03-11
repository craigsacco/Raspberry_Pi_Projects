# FRAM Demonstration

## About

This is a demonstration of a Python script interfacing with an SPI device connected
to a Raspberry Pi.

## Devices

The **Cypress FM25L04B** ferro-magnetic RAM IC has 512 bytes of non-volatile memory
connected to SPI device 0 connected to port 0 (/CS pin connected to CE0 pin on RPi),
the write-protect pin is wired to ground and the hold pin connected to GPIO23.

## Libraries

* **Adafruit_Python_PureIO** - provides low-level **ioctl**-based access to the
  I<sup>2</sup>C bus on the Raspberry Pi
* **Adafruit_Python_GPIO** - provides a flexible wrapper around RPi.GPIO and bus
  interfaces on the Raspberry Pi

## Prerequisites

* Image an SD card using the latest **Raspbian Jessie Lite** release
  (https://www.raspberrypi.org/downloads/raspbian)
* Download the following dependencies using **APT**:
  * **python-spidev** - provides user-mode tools for interacting with the SPI bus
* Use **raspi-config** to do the following:
  * Expand the filesystem to occupy the entire SD card
  * Enable the SPI bus kernel module on startup
