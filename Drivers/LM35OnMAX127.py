# -*- coding: utf-8 -*-


class LM35OnMAX127(object):

    OFFSET_V_0C = 0.0
    GAIN_VpC = 0.01

    def __init__(self, adc, channel):
        self.__name__ = "LM35"
        self._adc = adc
        self._channel = channel

    def get_data(self):
        # FIXME: should be using bipolar conversion, but I cannot seem to
        # FIXME: get the expected transfer function
        self._adc.start_conversion(channel=self._channel, bipolar=False)
        data = self._adc.get_data()
        temperature = (data["voltage"] - LM35OnMAX127.OFFSET_V_0C) / \
                      LM35OnMAX127.GAIN_VpC
        data.update({ "temperature": temperature, "temperature_uom": u"°C" })
        return data

    def get_temperature(self):
        return self.get_data()["temperature"]