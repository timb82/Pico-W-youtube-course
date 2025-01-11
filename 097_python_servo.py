from machine import Pin
from time import sleep_us
import rp2

PIN_SRVO = 20

# Example in python
servo = Pin(PIN_SRVO, Pin.OUT)
while True:
    angle = 90
    pw = int(angle * 2000 / 180 + 500)
    servo.on()
    sleep_us(pw)
    servo.off()
    sleep_us(20_000 - pw)
