from machine import Pin
from utime import sleep

led = Pin(14, Pin.OUT)

while True:
    try:
        led.toggle()
        print(led.value())
        sleep(0.8)
    except KeyboardInterrupt:
        break
