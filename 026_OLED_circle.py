from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from math import sin, cos, radians as rad


i2c = I2C(id=1, sda=Pin(6), scl=Pin(7))
disp = SSD1306_I2C(128, 64, i2c)

# disp.ellipse(64, 32, 20, 20, 1)
x0 = 64
y0 = 32
r = 20


def circle(x0, y0, r, start=0, stop=360, step=1):
    for deg in range(start, stop, step):
        x = int(x0 + r * cos(rad(deg)))
        y = int(y0 + r * sin(rad(deg)))
        disp.pixel(x, y, 1)
    disp.show()


for i in range(6):
    circle(x0, y0, r + i, step=30)

for i in range(6):
    circle(x0, y0, r + i, start=2, stop=362, step=30)

for i in range(6):
    circle(x0, y0, r + i, start=-2, stop=358, step=30)
