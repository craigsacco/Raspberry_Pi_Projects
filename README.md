# Raspberry Pi Projects

## About

This is a set of demonstration projects for using Python to interact with hardware
connected to a Raspberry Pi.

## Projects

The following projects are demonstrated:
* [**Simple Demos**](Projects/SimpleDemos) - small demonstration modules for testing devices
  * [**GPIO**](Projects/SimpleDemos/GPIO) - a simple demo with a pair of digital inputs and outputs
  * [**I2C_DS1624**](Projects/SimpleDemos/I2C_DS1624) - a single DS1624 serial temperature sensor
  * [**I2C_EEPROM**](Projects/SimpleDemos/I2C_EEPROM) - a single 24LC256 serial EEPROM device
  * [**SPI_FRAM**](Projects/SimpleDemos/SPI_FRAM) - a single FM25L04B serial ferro-magnetic RAM device
  * [**SPI_Flash**](Projects/SimpleDemos/SPI_Flash) - a single M25PX80 serial FLASH device
* [**Weather Station**](Projects/WeatherStation) - weather station demonstration
  with numerous sensors, GPS, a character LCD display and a REST/web interface

## Drivers

The following drivers are provided by this project:

Driver | Part # | Description | Interface
--- | --- | --- | ---
[DS1624](Drivers/DS1624.py) | Maxim DS1624 | Digital temperature sensor | I2C
[DS1803](Drivers/DS1803.py) | Maxim DS1803 | Dual digital potentiometers | I2C
[EE24LC256](Drivers/EE24LC256.py) | Microchip 24LC256 | 256-kilobit serial EEPROM | I2C
[FM25L04B](Drivers/FM25L04B.py) | Cypress FM25L04B | 512-byte serial ferro-magnetic RAM | SPI
[HIH3610OnMAX127](Drivers/HIH3610OnMAX127.py) | Honeywell HIH-3610 | Analog humidity sensor | Analog Input on MAX127
[LM35OnMAX127](Drivers/LM35OnMAX127.py) | TI LM35 | Analog temperature sensor | Analog Input on MAX127
[M25PX80](Drivers/M25PX80.py) | Micron M25PX80 | 1MB serial FLASH | SPI
[MAX127](Drivers/MAX127.py) | Maxim MAX127 | 12-bit analog-to-digital converter | I2C
[MS5534](Drivers/MS5534.py) | Intersema MS5534 | Digital barometric pressure sensor | Bit-Bash Serial
[SimpleLED](Drivers/SimpleLED.py) | N/A | Simple LED driver | Digital Output |
