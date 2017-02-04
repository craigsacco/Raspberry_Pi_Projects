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

    class ConversionException(Exception):
        pass

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
        result = self._gpio.wait_for_edge_with_timeout(self._miso, GPIO.FALLING, 1000)
        if result is None:
            raise MS5534.ConversionException()

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
        try:
            pressure_raw = 0#self.perform_pressure_conversion()
            temperature_raw = 0#self.perform_temperature_conversion()
            calibration_words = [self.get_calibration_word(i) for i in
                                 range(len(MS5534.SEQS_CALIBRATION_WORD))]
            self.send_reset()
            coefficient1 = (calibration_words[0] >> 1) & 0x7fff
            coefficient2 = ((calibration_words[2] & 0x3f) << 6) +\
                           (calibration_words[2] & 0x3f)
            coefficient3 = (calibration_words[3] >> 6) & 0x3ff
            coefficient4 = (calibration_words[2] >> 6) & 0x3ff
            coefficient5 = ((calibration_words[0] & 0x1) << 6) +\
                           ((calibration_words[1] >> 6) & 0x3ff)
            coefficient6 = (calibration_words[1] >> 6) & 0x3ff
            print pressure_raw, temperature_raw, calibration_words
            return {
                "pressure_raw": pressure_raw,
                "temperature_raw": temperature_raw,
                "calibration1": calibration_words[0],
                "calibration2": calibration_words[1],
                "calibration3": calibration_words[2],
                "calibration4": calibration_words[3],
                "coefficient1": coefficient1,
                "coefficient2": coefficient2,
                "coefficient3": coefficient3,
                "coefficient4": coefficient4,
                "coefficient5": coefficient5,
                "coefficient6": coefficient6,
            }
        except MS5534.ConversionException:
            return {}
