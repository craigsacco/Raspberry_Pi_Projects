# Invetech Sofware Resource Group Construction Pillar - Raspberry Pi Demo

## About

This is a demonstration project to extol the virtues of the Raspberry Pi
to members of the Invetech Software Resource Group.

## Devices

The following devices are demonstrated:
* **Maxim DS1624** - a digital thermometer (I<sup>2</sup>C devices on address
  0x48)
* **Intersema MS5534** - a digital barometer with integrated thermometer (SPI-like
  interface using bit-bash I/O)
  * with a **Maxim DS32KHZ** providing a high-precision 32.768kHz clock
* **Maxim DS1803** - a dual-10K digital potentiometer (I<sup>2</sup>C devices on
  address 0x29)
  * with two LED's pulled up to 5V with an inline 270R resistor
* **Maxim MAX127** - an 8-channel 12-bit ADC (I<sup>2</sup>C devices on address
  0x28)
  * with two **TI LM35** temperature sensors
  * with a **Honeywell HIH-3610** humidity sensor, amplified by a **TI LM324**
    op-amp in a unity gain configuration
* **Adafruit RGB LCD Pi Plate** (https://www.adafruit.com/product/1110)
  * with a 16x2 dot matrix character LCD display, controlled by a **Hitachi
    HD44780** LCD controller
  * with a **Microchip MCP23017** GPIO expander for I/O control of the LCD
    controller (I<sup>2</sup>C devices on address 0x20)
* **Waveshare UART GPS Module** (http://www.waveshare.com/wiki/UART_GPS_NEO-7M-C)
  * with a **u-blox NEO-7M-C** GPS module
  * with a **Waveshare UART TTL-to-USB** expansion board communicating to the
    GPS module via TTL, and the Raspberry Pi via USB using character device
    */dev/ttyUSB0*
* Three LED's directly connected to a digital output via a 330R resistor

On top of this, a **Waveshare RS-232** expansion board provides RS-232
connectivity between the Raspberry Pi and a PC via a **Maxim MAX3232** IC.

## Libraries

* **Adafruit_Python_PureIO** - provides low-level **ioctl**-based access to the
  I<sup>2</sup>C bus on the Raspberry Pi
* **Adafruit_Python_GPIO** - provides a flexible wrapper around RPi.GPIO and bus
  interfaces on the Raspberry Pi
* **Adafruit_Python_CharLCD** - provides an API for controlling a character LCD
  display
* **web.py** - provides a lightweight HTTP server with flexible GET/POST handling
* **gps3** - provides an interface for decoding data from **gpsd**
* **geopy** - provides coordinates and geospatial tools for Python

## Prerequisites

* Image an SD card using the latest **Raspbian Jessie Lite** release
  (https://www.raspberrypi.org/downloads/raspbian)
* Download the following dependencies using **APT**:
  * **i2c-tools** - provides user-mode tools for interacting with the
    I<sup>2</sup>C bus
  * **python-rpi.gpio** - provides user-mode libraries to the GPIO header
    through Python
  * **python-spidev** - provides user-mode libraries for accessing an SPI bus
    through Python
  * **gpsd** - provides user-mode access to a NEMA-compatible GPS receiver via
    a TCP socket
    * modify **/etc/default/gpsd** and set **DEVICES** to */dev/ttyUSB0*
    * restart the service by running **sudo systemctl restart gpsd.service**
* Use **raspi-config** to do the following:
  * Expand the filesystem to occupy the entire SD card
  * Enable the I<sup>2</sup>C bus kernel module on startup
  * Enable the SPI bus kernel module on startup
  * **DO NOT** disable the UART (unless you intend to not use it for kernel
    logging, or as a TTY)
