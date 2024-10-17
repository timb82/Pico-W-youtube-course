from machine import Pin
from utime import sleep


def snd_s():
    for n in range(3):
        led.on()
        sleep(0.2)
        led.off()
        sleep(0.2)


def snd_o():
    for n in range(3):
        led.on()
        sleep(1)
        led.off()
        sleep(0.2)


led = Pin(15, Pin.OUT)

while True:
    try:
        snd_s()
        sleep(0.3)
        snd_o()
        sleep(0.3)
        snd_s()
        sleep(2)
    except KeyboardInterrupt:
        break
