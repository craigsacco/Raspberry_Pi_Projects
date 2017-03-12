# Serial EEPROM Demonstration

## About

This is a demonstration of a Python script interfacing with simple GPIO devices
connected to a Raspberry Pi.

## Devices

The following hardware is connected to the following pin assignments on the
Raspberry Pi:
* 2 x micro-switches > connected to GPIO22 and GPIO25
* 2 x LEDs > connected to GPIO17 and GPIO27

## Libraries

* **Adafruit_Python_GPIO** - provides a flexible wrapper around RPi.GPIO and bus
  interfaces on the Raspberry Pi

## Prerequisites

* Image an SD card using the latest **Raspbian Jessie Lite** release
  (https://www.raspberrypi.org/downloads/raspbian)
* Download the following dependencies using **APT**:
  * **python-gevent** - provides co-routine functionality within Python
