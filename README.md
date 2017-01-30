# About

This is a demonstration project to extol the virtues of the Raspberry Pi
to members of the Invetech Software Resource Group

# Prerequisites

* A Raspberry Pi in headless mode
* An SD card with Raspbian Lite installed

# Setting up a Development Machine

* Install *PuTTY* for terminal emulation
* Install *sshfs* via APT to mount remote filesystems via SSH
  * Mount using the following command: `sshfs -o nonempty pi@ip-of-rpi:/home/pi /path/to/mount`
* Install *PyCharm* via GetDeb (http://www.getdeb.net/software/pycharm)

# Connect using a Serial Console

* Start PuTTY and setup a session with the following settings:
  * Serial device depends on how you've connected it - I use */dev/ttyS0*
  * 115200 baud, 8 data bits, no parity, one stop bit, no flow control
  * No local echo
* Through PuTTY, login with the following credentials:
  * Username: pi
  * Password: raspberry

# Raspbian Lite Setup

* It is recommended that you install *i2c-tools* via APT
* The following should be configured through *raspi-config*:
  * Enable I2C
  * Enable SPI
  * Enable SSH
  * Expand filesystem
  * **DO NOT** disable the UART (or else the serial console will no longer
   work)