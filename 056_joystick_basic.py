from machine import Pin, ADC
from utime import sleep_ms
import math

JOY_X_PIN = 27
JOY_Y_PIN = 26
JOY_SW_PIN = 17


class Joystick:
    def __init__(self, x_pin, y_pin, sw_pin):
        self._x = ADC(x_pin)
        self._y = ADC(y_pin)
        self._sw = Pin(sw_pin, Pin.IN, Pin.PULL_UP)

    @property
    def sw(self):
        return self._sw.value()

    @property
    def x(self):
        return self._x.read_u16()

    @property
    def y(self):
        return self._y.read_u16()


joy = Joystick(JOY_X_PIN, JOY_Y_PIN, JOY_SW_PIN)

while True:
    print(f"{joy.x:05d}\t{joy.y:05d}\t{joy.sw*50000}")
    sleep_ms(100)


"""
xmin=288
xmax = 65535
x0=29875


ymin = 288
y max 65535
y0 = 31127?"""
