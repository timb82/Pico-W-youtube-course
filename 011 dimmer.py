from machine import PWM, Pin, ADC
from utime import sleep
from math import log10

R_PIN = 11
Y_PIN = 12
G_PIN = 13
POT_PIN = 28  # ADC a
STEPS = 100

fade_factor = STEPS * log10(2) / log10(STEPS)


def brightness(level, A=100):
    duty = (pow(2, level / fade_factor) - 1) / STEPS
    if duty >= 0.99:
        duty = 1
    if duty < 0.0:
        duty = 0
    return A * duty


def readADC(A=100, max=0.999, min=0.001):
    val = A / 65227 * (pot.read_u16() - 269)
    if val > A * max:
        val = A
    if val < A * min:
        val = 0
    return val


pot = ADC(POT_PIN)
led_r = PWM(Pin(R_PIN))
led_r.freq(1000)
led_r.duty_u16(0)

led_g = PWM(Pin(G_PIN))
led_g.freq(1000)
led_g.duty_u16(0)

# led_y = Pin(Y_PIN, Pin.OUT)
# leds = [led_g, led_y, led_r]

while True:
    try:
        val = readADC()
        print(brightness(val))
        duty1 = brightness(val) * 2**16 / 100
        duty2 = brightness(65536 * (1 - val / 100)) * 2**16 / 100
        print(duty2)
        duty2 = brightness(val) * 2**16 / 100
        print(f"{round(3.3 / (2**16 - 1) * duty1,2):.02f} V")
        led_r.duty_u16(int(round(duty1)))
        led_g.duty_u16(int(round(duty2)))
        sleep(0.1)
    except KeyboardInterrupt:
        led_g.duty_u16(0)
        led_r.duty_u16(0)
        break
