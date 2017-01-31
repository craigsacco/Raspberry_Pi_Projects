#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(1, 'Libraries')
sys.path.insert(1, 'Libraries/Adafruit_Python_PureIO')
sys.path.insert(1, 'Libraries/Adafruit_Python_GPIO')
sys.path.insert(1, 'Libraries/webpy')

import time, web, json, threading
from DS1624 import DS1624
from MAX127 import MAX127
from LM35OnMAX127 import LM35OnMAX127
from HIH3610OnMAX127 import HIH3610OnMAX127


class StationServer(object):

    DATA = {}
    DATA_MUTEX = threading.Lock()

    class DataService:

        def GET(self):
            web.header("Content-Type", "text/json")
            StationServer.DATA_MUTEX.acquire()
            data = StationServer.DATA
            StationServer.DATA_MUTEX.release()
            return json.dumps(data)

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

    def __init__(self):
        self._server = web.application(StationServer.URLS, locals())
        self._ds1624 = DS1624(address=0x48)
        self._max127 = MAX127(address=0x28)
        self._lm35_1 = LM35OnMAX127(adc=self._max127, channel=0)
        self._lm35_2 = LM35OnMAX127(adc=self._max127, channel=1)
        self._hih3610 = HIH3610OnMAX127(adc=self._max127, channel=2)

    def start_devices(self):
        self._ds1624.start_conversions()

    def stop_devices(self):
        self._ds1624.stop_conversions()
        self._max127.power_down()

    def update_data(self):
        StationServer.DATA_MUTEX.acquire()
        StationServer.DATA = {
            "ds1624": self._ds1624.get_data(),
            "lm35_1": self._lm35_1.get_data(),
            "lm35_2": self._lm35_2.get_data(),
            "hih3610": self._hih3610.get_data(),
        }
        StationServer.DATA_MUTEX.release()

    def background_acquisition(self):
        self._acquire = True
        while self._acquire:
            time.sleep(2)
            self.update_data()

    def run_server(self):
        self.start_devices()
        self._thread = threading.Thread(target=self.background_acquisition)
        self._thread.start()
        self._server.run()

    def stop_server(self):
        self._server.stop()
        self._acquire = False
        self._thread.join()
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
