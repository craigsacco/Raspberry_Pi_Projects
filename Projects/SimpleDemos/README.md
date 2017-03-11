# DS1624 Demonstration

## About

This is a demonstration of a Python script interfacing with an I<sup>2</sup>C
device connected to a Raspberry Pi.

## Devices

The **Maxim DS1624** digital thermometer is being demonstrated. The A0, A1 and A2
pins are tied to ground, yielding an I<sup>2</sup>C device address of 0x48.

## Libraries

* **Adafruit_Python_PureIO** - provides low-level **ioctl**-based access to the
  I<sup>2</sup>C bus on the Raspberry Pi
* **Adafruit_Python_GPIO** - provides a flexible wrapper around RPi.GPIO and bus
  interfaces on the Raspberry Pi

## Prerequisites

* Image an SD card using the latest **Raspbian Jessie Lite** release
  (https://www.raspberrypi.org/downloads/raspbian)
* Download the following dependencies using **APT**:
  * **i2c-tools** - provides user-mode tools for interacting with the
    I<sup>2</sup>C bus
* Use **raspi-config** to do the following:
  * Expand the filesystem to occupy the entire SD card
  * Enable the I<sup>2</sup>C bus kernel module on startup
