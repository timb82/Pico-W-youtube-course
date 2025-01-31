from machine import Pin
from time import sleep_us, ticks_us, ticks_diff

TRIG_PIN = 16
ECHO_PIN = 17

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)


def distance():
    trig.low()
    sleep_us(2)
    trig.high()
    sleep_us(10)
    trig.low()
    while echo.value() == 0:
        pass
    time1 = ticks_us()
    while echo.value() == 1:
        pass
    time2 = ticks_us()

    ping_time = ticks_diff(time2, time1)
    return 0.0343 * ping_time / 2


while True:
    print(f"Distance: {distance():0.2f} cm")
    sleep_us(300_000)
