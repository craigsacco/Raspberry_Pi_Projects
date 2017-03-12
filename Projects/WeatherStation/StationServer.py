#!/usr/bin/python
# -*- coding: utf-8 -*-

# monkey patch python libraries to use co-routines instead of threads
from gevent import monkey
monkey.patch_all()

# import libraries from git submodules
import sys
sys.path.insert(1, '../../Drivers')
sys.path.insert(1, '../../Libraries/Adafruit_Python_PureIO')
sys.path.insert(1, '../../Libraries/Adafruit_Python_GPIO')
sys.path.insert(1, '../../Libraries/Adafruit_Python_CharLCD')
sys.path.insert(1, '../../Libraries/geopy')
sys.path.insert(1, '../../Libraries/gps3')
sys.path.insert(1, '../../Libraries/webpy')

import web, json, threading, gevent
from Adafruit_CharLCD import SELECT as LCD_BTN_SELECT
from Adafruit_CharLCD.Adafruit_CharLCD import Adafruit_CharLCDPlate
from gps3.gps3 import GPSDSocket
from geopy.format import format_degrees
from DS1624 import DS1624
from MAX127 import MAX127
from LM35OnMAX127 import LM35OnMAX127
from HIH3610OnMAX127 import HIH3610OnMAX127
from MS5534 import MS5534
from SimpleLED import SimpleLED
from DS1803 import DS1803


class StationServer(object):

    DATA = {}
    DATA_MUTEX = threading.Lock()
    GPS = {}
    GPS_MUTEX = threading.Lock()

    class DataService:

        def GET(self):
            web.header("Content-Type", "text/json")
            StationServer.DATA_MUTEX.acquire()
            data = StationServer.DATA
            StationServer.DATA_MUTEX.release()
            return json.dumps(data, sort_keys=True,
                              indent=4, separators=(',', ': '))

    class UIService:

        def GET(self):
            try:
                web.header("Content-Type", "text/html")
                return open("StationServer.html", "rb").read()
            except:
                raise web.notfound()

    URLS = (
        "/Data",        DataService,
        "/index.htm",   UIService,
        "/index.html",  UIService,
        "/",            UIService,
    )

    DISPMODE_PRESSURE_HUMIDITY = 0
    DISPMODE_TEMPERATURE_ANALOG = 1
    DISPMODE_TEMPERATURE_DIGITAL = 2
    DISPMODE_GPS = 3
    DISPMODE_COUNT = 4

    def __init__(self):
        self._server = web.application(StationServer.URLS, locals())
        self._ds1624 = DS1624(i2c_address=0x48)
        self._max127 = MAX127(i2c_address=0x28)
        self._lm35_1 = LM35OnMAX127(adc=self._max127, channel=0)
        self._lm35_2 = LM35OnMAX127(adc=self._max127, channel=1)
        self._hih3610 = HIH3610OnMAX127(adc=self._max127, channel=2)
        self._ms5534 = MS5534(sclk=22, miso=27, mosi=17)
        self._led_1 = SimpleLED(pin=18)
        self._led_2 = SimpleLED(pin=23)
        self._led_3 = SimpleLED(pin=24)
        self._leds = [self._led_1, self._led_2, self._led_3]
        self._lcdplate = Adafruit_CharLCDPlate(address=0x20)
        self._dispmode = StationServer.DISPMODE_PRESSURE_HUMIDITY
        self._pots = DS1803(i2c_address=0x29, variant=DS1803.VARIANT_10K)
        self._gps = GPSDSocket()

    def start_devices(self):
        self._ds1624.start_conversions()
        self._ms5534.send_reset()
        self._lcdplate.clear()
        self._gps.connect()
        self._gps.watch(gpsd_protocol="json", devicepath="/dev/ttyUSB0")

    def stop_devices(self):
        self._ds1624.stop_conversions()
        self._max127.power_down()
        self._lcdplate.clear()
        self._lcdplate.set_color(0.0, 0.0, 0.0)
        self._gps.close()

    def update_data(self):
        StationServer.DATA_MUTEX.acquire()
        StationServer.GPS_MUTEX.acquire()
        StationServer.DATA = {
            "ds1624": self._ds1624.get_data(),
            "lm35_1": self._lm35_1.get_data(),
            "lm35_2": self._lm35_2.get_data(),
            "hih3610": self._hih3610.get_data(),
            "ms5534": self._ms5534.get_data(),
            "gps": StationServer.GPS,
        }
        StationServer.GPS_MUTEX.release()
        StationServer.DATA_MUTEX.release()
        self.update_display()

    def update_display(self):
        if self._lcdplate.is_pressed(LCD_BTN_SELECT):
            self._dispmode += 1
            self._lcdplate.clear()
            if self._dispmode == StationServer.DISPMODE_COUNT:
                self._dispmode = 0
        if self._dispmode == StationServer.DISPMODE_PRESSURE_HUMIDITY:
            self._lcdplate.set_color(0.0, 0.0, 1.0)
            self._lcdplate.set_cursor(0, 0)
            self._lcdplate.message("Hum:  {0:.2f} {1} ".format(
                StationServer.DATA["hih3610"]["humidity"],
                StationServer.DATA["hih3610"]["humidity_uom"].encode("ascii", "ignore")
            ))
            self._lcdplate.set_cursor(0, 1)
            self._lcdplate.message("Pres: {0:.2f} {1} ".format(
                StationServer.DATA["ms5534"]["pressure"],
                StationServer.DATA["ms5534"]["pressure_uom"].encode("ascii", "ignore")
            ))
        elif self._dispmode == StationServer.DISPMODE_TEMPERATURE_ANALOG:
            self._lcdplate.set_color(1.0, 0.0, 0.0)
            self._lcdplate.set_cursor(0, 0)
            self._lcdplate.message("Ta1: {0:.2f} {1} ".format(
                StationServer.DATA["lm35_1"]["temperature"],
                StationServer.DATA["lm35_1"]["temperature_uom"].encode("ascii", "ignore")
            ))
            self._lcdplate.set_cursor(0, 1)
            self._lcdplate.message("Ta2: {0:.2f} {1} ".format(
                StationServer.DATA["lm35_2"]["temperature"],
                StationServer.DATA["lm35_2"]["temperature_uom"].encode("ascii", "ignore")
            ))
        elif self._dispmode == StationServer.DISPMODE_TEMPERATURE_DIGITAL:
            self._lcdplate.set_color(1.0, 1.0, 0.0)
            self._lcdplate.set_cursor(0, 0)
            self._lcdplate.message("Tdt: {0:.2f} {1} ".format(
                StationServer.DATA["ds1624"]["temperature"],
                StationServer.DATA["ds1624"]["temperature_uom"].encode("ascii", "ignore")
            ))
            self._lcdplate.set_cursor(0, 1)
            self._lcdplate.message("Tps: {0:.2f} {1} ".format(
                StationServer.DATA["ms5534"]["temperature"],
                StationServer.DATA["ms5534"]["temperature_uom"].encode("ascii", "ignore")
            ))
        elif self._dispmode == StationServer.DISPMODE_GPS:
            self._lcdplate.set_color(0.0, 1.0, 0.0)
            self._lcdplate.set_cursor(0, 0)
            dms_format = "%(degrees)dd %(minutes)dm %(seconds)ds"
            latitude = "N/A"
            longitude = "N/A"
            if "lat" in StationServer.DATA["gps"]["TPV"].keys():
                latitude = format_degrees(StationServer.DATA["gps"]["TPV"]["lat"], fmt=dms_format)
            if "lon" in StationServer.DATA["gps"]["TPV"].keys():            
                longitude = format_degrees(StationServer.DATA["gps"]["TPV"]["lon"], fmt=dms_format)
            self._lcdplate.message("La: {0}  ".format(latitude))
            self._lcdplate.set_cursor(0, 1)
            self._lcdplate.message("Ln: {0}  ".format(longitude))

    def background_acquisition(self):
        print "Started sensor acquisition"
        while self._running:
            gevent.sleep(2)
            self.update_data()
        print "Stopped sensor acquisition"

    def led_sequencer(self):
        print "Started LED sequencer"
        routine = 0
        iteration = 0
        index = 0
        while self._running:
            gevent.sleep(0.2)
            if routine == 0:
                if self._leds[index].get_state():
                    self._leds[index].off()
                    index += 1
                else:
                    self._leds[index].on()
                if index == len(self._leds):
                    index = 0
                    iteration += 1
                if iteration == 3:
                    routine = 1
                    iteration = 0
            elif routine == 1:
                if index == 0:
                    for led in self._leds:
                        led.on()
                    index += 1
                elif index == 1:
                    for led in self._leds:
                        led.off()
                    iteration += 1
                    index = 0
                if iteration == 3:
                    routine = 0
                    iteration = 0
        for led in self._leds:
            led.off()
        print "Stopped LED sequencer"

    def led_dimmer(self):
        print "Started LED dimmer"
        pot_resistances = [0, 100, 250, 600, 1500, 4000, 1500,
                           600, 250, 100]
        index = 0
        while self._running:
            gevent.sleep(0.1)
            self._pots.set_both_pots_resistance(pot_resistances[index])
            index += 1
            if index == len(pot_resistances):
                index = 0
        self._pots.set_both_pots_resistance(0)
        print "Stopped LED dimmer"

    def gps_acquisition(self):
        print "Started GPS acquisition"
        for data in self._gps:
            if data:
                packet = json.loads(data)
                StationServer.GPS_MUTEX.acquire()
                StationServer.GPS[packet["class"]] = packet
                StationServer.GPS_MUTEX.release()
            else:
                gevent.sleep(0.1)
            if not self._running:
                break
        print "Stopped GPS acquisition"

    def run_server(self):
        self._running = True
        self.start_devices()
        self._threads = [
            gevent.spawn(self.background_acquisition),
            gevent.spawn(self.led_sequencer),
            gevent.spawn(self.led_dimmer),
            gevent.spawn(self.gps_acquisition)
        ]
        self._server.run()

    def stop_server(self):
        self._running = False
        gevent.joinall(self._threads)
        self._server.stop()
        self.stop_devices()


def main():
    server = StationServer()
    result = 0
    try:
        server.run_server()
    except KeyboardInterrupt:
        result = 0
    except:
        result = 1
    finally:
        server.stop_server()
    return result


if __name__ == "__main__":
    sys.exit(main())
