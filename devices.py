from machine import Pin, ADC
from time import sleep
from math import atan2, sqrt, pi


class LED:
    def __init__(self, led_pin):
        self._pin = Pin(led_pin, Pin.OUT)

    def _close(self):
        self._pin.off()

    def blink(self, blinks_no, delay):
        for i in range(0, blinks_no):
            self._pin.on()
            sleep(delay)
            self._pin.off()
            sleep(delay)

    def on(self):
        self._pin.on()

    def off(self):
        self._pin.off()


class Joystick:
    def __init__(
        self,
        x_pin,
        y_pin,
        sw_pin,
        xmin=288,
        xmax=65535,
        ymin=288,
        ymax=65535,
        dead_x=12,
        dead_y=7,
    ):
        self._x = ADC(x_pin)
        self._y = ADC(y_pin)
        self._xmin = xmin
        self._xmax = xmax
        self._ymin = ymin
        self._ymax = ymax
        self.dead_x = dead_x
        self.dead_y = dead_y
        self._sw = Pin(sw_pin, Pin.IN, Pin.PULL_UP)
        self._x_cal = self._coefs(self._xmin, self._xmax)
        self._y_cal = self._coefs(self._ymin, self._ymax)
        self._dead_x = self.dead_x
        self._dead_y = self.dead_y

    def _coefs(self, ax_min, ax_max, val_min=-100, val_max=100):
        a = (val_max - val_min) / (ax_max - ax_min)
        b = a * ax_max + val_min
        return (a, -b)

    def _scale(self, value, cal_coeffs):
        return cal_coeffs[0] * value + cal_coeffs[1]

    @property
    def sw(self):
        return self._sw.value()

    @property
    def x(self):
        val = self._scale(self._x, self._x_cal)
        if abs(val) >= self._dead_x:
            return val
        else:
            return 0

    @property
    def y(self):
        val = self._scale(self._y, self._y_cal)
        if abs(val) >= self._dead_y:
            return val
        else:
            return 0

    @property
    def pos(self):
        return (
            self._scale(self._x.read_u16(), self._x_cal),
            self._scale(self._y.read_u16(), self._y_cal),
        )

    @property
    def mag(self):
        p = self.pos
        return sqrt(p[0] ** 2 + p[1] ** 2)

    @property
    def angle(self):
        m = self.mag
        if m < 5:
            return 0
        a = atan2(self.pos[1], self.pos[0]) / 2 / pi * 360
        if a < 0:
            a = a + 360
        return a
