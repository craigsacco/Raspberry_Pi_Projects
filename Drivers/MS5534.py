# -*- coding: utf-8 -*-

import Adafruit_GPIO.GPIO as GPIO


class MS5534(object):

    SEQS_CALIBRATION_WORD = [
        [False, True, False, True, False, True],
        [False, True, False, True, True, False],
        [False, True, True, False, False, True],
        [False, True, True, False, True, False],
    ]
    SEQ_PRESSURE_CONVERSION = [True, False, True, False]
    SEQ_TEMPERATURE_CONVERSION = [True, False, False, True]

    def __init__(self, sclk, miso, mosi, gpio=None):
        self._gpio = gpio or GPIO.get_platform_gpio()
        self._sclk = sclk
        self._miso = miso
        self._mosi = mosi
        self._gpio.setup(self._sclk, GPIO.OUT)
        self._gpio.setup(self._miso, GPIO.IN)
        self._gpio.setup(self._mosi, GPIO.OUT)
        self._gpio.output(self._sclk, GPIO.LOW)
        self._gpio.output(self._mosi, GPIO.LOW)

    def send_clock(self):
        self._gpio.output(self._sclk, GPIO.HIGH)
        self._gpio.output(self._sclk, GPIO.LOW)

    def send_bit(self, value):
        self._gpio.output(self._mosi, GPIO.HIGH if value else GPIO.LOW)
        self.send_clock()

    def get_miso(self):
        return self._gpio.is_high(self._miso)

    def get_bit(self):
        self.send_clock()
        return self.get_miso()

    def wait_for_conversion_completion(self):
        self._gpio.wait_for_edge(self._miso, GPIO.FALLING)

    def send_command_sequence(self, seq):
        # sequence:
        #  * send 0b111
        #  * send sequence of bits
        #  * send 0b000
        for i in range(3):
            self.send_bit(True)
        for i in range(len(seq)):
            self.send_bit(seq[i])
        for i in range(3):
            self.send_bit(False)

    def get_value(self, width):
        value = 0
        for i in range(width):
            value <<= 1
            value += (1 if self.get_bit() else 0)
        return value

    def get_calibration_word(self, index):
        # sequence:
        #  * send command sequence
        #  * send a single clock - check that MISO is high
        #  * read 16 bits
        #  * send a single clock
        self.send_command_sequence(MS5534.SEQS_CALIBRATION_WORD[index])
        self.send_clock()
        assert self.get_miso() == True
        value = self.get_value(16)
        self.send_clock()
        return value

    def perform_conversion(self, seq):
        # sequence:
        #  * send command sequence
        #  * send two clocks - check that MISO is high
        #  * wait for conversion to complete
        #  * read 16 bits
        #  * send a single clock
        self.send_command_sequence(seq)
        self.send_clock()
        self.send_clock()
        assert self.get_miso() == True
        self.wait_for_conversion_completion()
        value = self.get_value(16)
        self.send_clock()
        return value

    def perform_pressure_conversion(self):
        return self.perform_conversion(MS5534.SEQ_PRESSURE_CONVERSION)

    def perform_temperature_conversion(self):
        return self.perform_conversion(MS5534.SEQ_TEMPERATURE_CONVERSION)

    def send_reset(self):
        # sequence:
        #  * send alternating 0b10 8 times
        #  * send 0b00000
        for i in range(8):
            self.send_bit(True)
            self.send_bit(False)
        for i in range(5):
            self.send_bit(False)

    def get_data(self):
        pressure_raw = self.perform_pressure_conversion()
        temperature_raw = self.perform_temperature_conversion()
        equ_w1, equ_w2, equ_w3, equ_w4 =\
            [self.get_calibration_word(i) for i in
             range(len(MS5534.SEQS_CALIBRATION_WORD))]
        self.send_reset()
        equ_c1 = (equ_w1 >> 1) & 0x7fff
        equ_c2 = ((equ_w3 & 0x3f) << 6) + (equ_w4 & 0x3f)
        equ_c3 = (equ_w4 >> 6) & 0x3ff
        equ_c4 = (equ_w3 >> 6) & 0x3ff
        equ_c5 = ((equ_w1 & 0x1) << 6) + ((equ_w2 >> 6) & 0x3ff)
        equ_c6 = equ_w2 & 0x3f
        equ_ut1 = (8.0 * equ_c5) + 20224
        equ_dt = temperature_raw - equ_ut1
        equ_temp = 200 + ((equ_dt * (equ_c6 + 50)) / 1024.0)
        temperature = equ_temp / 10.0
        equ_off = (equ_c2 * 4.0) + (((equ_c4 - 512) * equ_dt) / 4096.0)
        equ_sens = equ_c1 + 24576 + ((equ_c3 * equ_dt) / 1024.0)
        equ_x = ((equ_sens * (pressure_raw - 7168)) / 16384.0) - equ_off
        equ_p = (equ_x * (10.0 / 32.0)) + 2500
        pressure = equ_p / 100.0
        return {
            "pressure_raw": pressure_raw,
            "temperature_raw": temperature_raw,
            "equ_w1": equ_w1,
            "equ_w2": equ_w2,
            "equ_w3": equ_w3,
            "equ_w4": equ_w4,
            "equ_c1": equ_c1,
            "equ_c2": equ_c2,
            "equ_c3": equ_c3,
            "equ_c4": equ_c4,
            "equ_c5": equ_c5,
            "equ_c6": equ_c6,
            "equ_ut1": equ_ut1,
            "equ_dt": equ_dt,
            "equ_temp": equ_temp,
            "temperature": temperature,
            "temperature_uom": u"°C",
            "equ_off": equ_off,
            "equ_sens": equ_sens,
            "equ_x": equ_x,
            "equ_p": equ_p,
            "pressure": pressure,
            "pressure_uom": u"kPa",
        }

    def get_pressure_only(self):
        return self.get_data()["pressure"]

    def get_temperature_only(self):
        return self.get_data()["temperature"]

    def get_pressure_and_temperature(self):
        data = self.get_data()
        return [data["pressure"], data["temperature"]]
