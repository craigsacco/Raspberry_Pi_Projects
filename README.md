# About

This is a demonstration project to extol the virtues of the Raspberry Pi
to members of the Invetech Software Resource Group

# Prerequisites

* A Raspberry Pi in headless mode
* An SD card with Raspbian Lite installed

# Setting up a Development Machine

* Install *PuTTY* and setup a serial connection to a Raspberry Pi using
  the following settings:
** 115200 baud, 8 data bits, no parity, one stop bit, no flow control
** No local echo
* Install *sshfs* to mount remote filesystems via SSH

# Raspbian Lite Setup

* It is recommended that you install *i2c-tools* from APT
* The following should be configured through *raspi-config*:
** Enable I2C
** Enable SPI
** Enable SSH
** Expand filesystem
** *DO NOT* disable the UART (or else the serial console will no longer
   work)