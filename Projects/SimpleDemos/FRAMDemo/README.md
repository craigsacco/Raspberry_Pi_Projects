# FRAM Demonstration

## About

This is a demonstration of a Python script interfacing with an SPI device connected
to a Raspberry Pi.

## Devices

The **Cypress FM25L04B** ferro-magnetic RAM IC has 512 bytes of non-volatile memory
with the following pin assignments to the Raspberry Pi:
* SCK/SI/SO > connected to the SPI0_SCLK, SPI0_MOSI and SPI0_MISO (respectively)
* /CS > connected to SPI0_CE0
* /WP > connected to 3.3V
* /HOLD > connected to GPIO23

The device will be accessible under Raspbian as the character device */dev/spidev0.0*
* the first **0** is the SPI bus number (connected to SPI0)
* the second **0** is the SPI port number on the bus (connected to the CE0 signal on
  the bus - bus is normally in tri-state unless the CE0 signal is driven low)

## Libraries

* **Adafruit_Python_PureIO** - provides low-level **ioctl**-based access to the
  I<sup>2</sup>C bus on the Raspberry Pi
* **Adafruit_Python_GPIO** - provides a flexible wrapper around RPi.GPIO and bus
  interfaces on the Raspberry Pi

## Prerequisites

* Image an SD card using the latest **Raspbian Jessie Lite** release
  (https://www.raspberrypi.org/downloads/raspbian)
* 
* Download the following dependencies using **APT**:
  * **python-spidev** - provides user-mode tools for interacting with the SPI bus
* Use **raspi-config** to do the following:
  * Expand the filesystem to occupy the entire SD card
  * Enable the SPI bus kernel module on startup
