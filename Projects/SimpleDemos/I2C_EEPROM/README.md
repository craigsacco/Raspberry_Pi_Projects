# Serial EEPROM Demonstration

## About

This is a demonstration of a Python script interfacing with an I<sup>2</sup>C
EEPROM device connected to a Raspberry Pi.

## Devices

The **Microchip 24LC256** EEPROM IC has 256-kilobit (32kB) of non-volatile memory
with the following pin assignments to the Raspberry Pi:
* SDA/SCL > connected to the I2C#_SDA and I2C#_SCL (respectively)
  * on the Raspberry Pi 1, pins 3 and 5 are wired to I2C0_SDA and I2C0_SCL
  * on the Raspberry Pi 2 and 3, pins 3 and 5 are wired to I2C1_SDA and I2C1_SCL
  * the Adafruit libraries is smart enough to detect the Raspberry Pi variant,
    and use the appropriate I<sup>2</sup>C bus
* A0/A1/A2 > connected to GND (I<sup>2</sup>C address set to 0x50)
* WP > connected to GND (permanently in writeable mode)

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
  * Enable the SPI bus kernel module on startup
