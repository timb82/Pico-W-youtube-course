from machine import Pin, ADC
from utime import sleep

R_PIN = 11
Y_PIN = 12
G_PIN = 13
POT_PIN = 28  # ADC a


def readADC(A=3.3):
    val = A / 65227 * (pot.read_u16() - 269)
    if val > A:
        val = A
    if val < 0:
        val = 0
    return val


pot = ADC(POT_PIN)
led_r = Pin(R_PIN, Pin.OUT)
led_y = Pin(Y_PIN, Pin.OUT)
led_g = Pin(G_PIN, Pin.OUT)
leds = [led_g, led_y, led_r]

while True:
    try:
        val = readADC(100)
        print(val)
        if val < 80:
            led_g.value(1)
            led_y.value(0)
            led_r.value(0)
        elif val < 95:
            led_g.value(0)
            led_y.value(1)
            led_r.value(0)
        elif val >= 95:
            led_g.value(0)
            led_y.value(0)
            led_r.value(1)
        sleep(0.1)

    except KeyboardInterrupt:
        for l in leds:
            l.off()
        print("bye")
        break
