from machine import Pin, ADC, PWM
from utime import sleep_ms
from math import acos, sqrt, pi, atan2
from sys import exit

JOY_X_PIN = 27
JOY_Y_PIN = 26
JOY_SW_PIN = 17
SERVO_PIN = 16

JOY_X_MIN = 288
JOY_X_MAX = 65535
JOY_Y_MIN = 288
JOY_Y_MAX = 65535
DEADZONE_X = 10.7  # % of range in each direction
DEADZONE_Y = 7.3  # % of range in each direction


class Joystick:
    def __init__(self, x_pin, y_pin, sw_pin):
        self._x = ADC(x_pin)
        self._y = ADC(y_pin)
        self._sw = Pin(sw_pin, Pin.IN, Pin.PULL_UP)
        self._x_cal = self._coefs(JOY_X_MIN, JOY_X_MAX)
        self._y_cal = self._coefs(JOY_Y_MIN, JOY_Y_MAX)
        self._dead_x = DEADZONE_X
        self._dead_y = DEADZONE_Y

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
        try:
            a = atan2(self.pos[1], self.pos[0]) / 2 / pi * 360
            if a < 0:
                a = a + 360
            return a
        except ValueError:
            print(f"values out of bound: {self.pos[1]}, {m}, {self.pos[1] / m}")
            exit(2)


def duty(angle):
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180
    return int(angle * 1e5 / 9 + 5e5)


ang = 90
joy = Joystick(JOY_X_PIN, JOY_Y_PIN, JOY_SW_PIN)
servo = PWM(Pin(SERVO_PIN))
servo.freq(50)
servo.duty_ns(duty(ang))

while True:
    # print(f"{joy.x:.1f}\t{joy.y:.1f}\t{(1-joy.sw)*100}")
    # print(f"x={joy.pos[0]}\ty={joy.pos[1]}\talpha={joy.angle} ")
    print(joy.pos[0], ang)
    if joy.pos[0] < -12 and ang <= 180:
        print("ping")
        ang = ang - joy.pos[0] / 10
    elif joy.pos[0] > 12 and ang >= 0:
        print("pong")
        ang = ang - joy.pos[0] / 10

    if ang > 180:
        ang = 180
    elif ang < 0:
        ang = 0
    servo.duty_ns(duty(ang))
    sleep_ms(50)


"""
ymin = -100
ymax = 100
xmin = int(input("min: "))
xmax = int(input("max: "))

a = (ymax-ymin)/(xmax-xmin)
b = a*xmax +ymin
print(f"y = {a} x + {b}")
"""

"""
xmin=288
xmax = 65535
x0=29875

ymin = 288
y max 65535
y0 = 31127?"""
