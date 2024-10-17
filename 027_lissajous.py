from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from math import sin, cos, radians as rad
from old_rotary import RotaryIRQ

CLK_PIN = 28
DT_PIN = 27
BTN_PIN = 26


i2c = I2C(id=1, sda=Pin(6), scl=Pin(7))
disp = SSD1306_I2C(128, 64, i2c)

rot = RotaryIRQ(
    pin_num_clk=28,
    pin_num_dt=27,
    min_val=0,
    max_val=6,
    reverse=True,
    range_mode=RotaryIRQ.RANGE_BOUNDED,
)

btn = Pin(BTN_PIN, Pin.IN, Pin.PULL_UP)
rot_old = rot.value()
btn_old = 1

x0 = 64
y0 = 32
r = 24
n1 = 1
n2 = 1
phase = 0
ph_adv = 0
ph_f = 0

while True:
    try:
        rot_new = rot.value()
        btn_new = btn.value()
        if ph_f == 0:
            disp.pixel(0, 63, 1)
        elif ph_f == 1:
            disp.pixel(64, 63, 1)
        else:
            disp.pixel(127, 63, 1)

        if btn_new == 0 and btn_old == 1:
            if ph_f < 2:
                ph_f += 1
            else:
                ph_f = 0

            if ph_f == 0:
                rot.set(value=ph_adv)
            elif ph_f == 1:
                rot.set(value=n1)
            else:
                rot.set(value=n2)

        btn_old = btn_new

        if rot_old is not rot_new:
            rot_old = rot_new
            if ph_f == 0:
                ph_adv = rot_new
            elif ph_f == 1:
                n1 = rot_new
            else:
                n2 = rot_new

        for deg in range(0, 360, 1):
            x = int(r * cos(n1 * rad(deg) + rad(phase)) + x0)
            y = int(r * sin(n2 * rad(deg)) + y0)
            disp.pixel(x, y, 1)

        phase += ph_adv
        disp.show()
        disp.fill(0)
        # print(
        #     f"n={n},\tphase advance = {ph_adv},\tcontrolling: {'phase' if ph_f else "freq"}"
        # )
    except KeyboardInterrupt:
        disp.fill(0)
        disp.poweroff()
        break
