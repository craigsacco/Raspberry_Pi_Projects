#!/usr/bin/python
# -*- coding: utf-8 -*-

# import libraries from git submodules
import sys
sys.path.insert(1, '../../../Libraries/Adafruit_Python_GPIO')

import gevent
import Adafruit_GPIO.GPIO as GPIO


GPIO_SWITCH1 = 22
GPIO_SWITCH2 = 25
GPIO_LED1 = 17
GPIO_LED2 = 27


def main():
    gpio = GPIO.get_platform_gpio()
    gpio.setup(GPIO_SWITCH1, GPIO.IN)
    gpio.setup(GPIO_SWITCH2, GPIO.IN)
    gpio.setup(GPIO_LED1, GPIO.OUT)
    gpio.setup(GPIO_LED2, GPIO.OUT)

    running = True

    def led_blinker():
        operations = [
            lambda: gpio.set_high(GPIO_LED1),
            lambda: gpio.set_low(GPIO_LED1),
            lambda: gpio.set_high(GPIO_LED2),
            lambda: gpio.set_low(GPIO_LED2),
        ]
        op_index = 0
        while running:
            operations[op_index]()
            op_index += 1
            if op_index == len(operations):
                op_index = 0
            gevent.sleep(0.5)

    def switch_poller():
        while running:
            switch1 = gpio.is_high(GPIO_SWITCH1)
            switch2 = gpio.is_high(GPIO_SWITCH2)
            print "switch states: sw1={0} sw2={1}".format(switch1, switch2)
            gevent.sleep(0.5)

    thread1 = gevent.spawn(led_blinker)
    thread2 = gevent.spawn(switch_poller)

    try:
        while True:
            gevent.sleep(1)
    except KeyboardInterrupt:
        running = False
        thread1.join()
        thread2.join()
    finally:
        pass


if __name__ == "__main__":
    sys.exit(main())
