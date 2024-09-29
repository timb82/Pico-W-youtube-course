from machine import Pin
from utime import sleep

led = Pin(15, Pin.OUT)

while True:
    try:
        led.toggle()
        sleep(0.8)
    except KeyboardInterrupt:
        break
