# -*- coding: utf-8 -*-


class HIH3610OnMAX127(object):

    OFFSET_V_0RHpc = 0.958
    GAIN_VpRHpc = 0.03068

    def __init__(self, adc, channel):
        self.__name__ = "HIH-3610"
        self._adc = adc
        self._channel = channel

    def get_data(self):
        self._adc.start_conversion(channel=self._channel)
        data = self._adc.get_data()
        humidity = (data["voltage"] - HIH3610OnMAX127.OFFSET_V_0RHpc) / \
                   HIH3610OnMAX127.GAIN_VpRHpc
        data.update({ "humidity": humidity, "humidity_uom": u"%RH" })
        return data

    def get_humidity(self):
        return self.get_data()["humidity"]