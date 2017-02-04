# -*- coding: utf-8 -*-

import Adafruit_GPIO.GPIO as GPIO


class SimpleLED(object):

    def __init__(self, pin, gpio=None):
        self._gpio = gpio or GPIO.get_platform_gpio()
        self._pin = pin
        self._gpio.setup(self._pin, GPIO.OUT)
        self._gpio.output(self._pin, GPIO.LOW)
        self._state = False

    def set(self, state):
        self._gpio.output(self._pin, GPIO.HIGH if state else GPIO.LOW)
        self._state = state

    def on(self):
        self.set(True)

    def off(self):
        self.set(False)

    def get_state(self):
        return self._state