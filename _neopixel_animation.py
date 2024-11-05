import neopixel
from machine import Pin
import time

PIX_PIN = 5
PIX_SIZE = 8

pix = neopixel.NeoPixel(Pin(PIX_PIN, Pin.OUT), PIX_SIZE)

red = [15,0,0]
green = [0,15,0]
blue = [0,0,15]
off = [0,0,0]

try:
    while True:

        for i in range(PIX_SIZE):
            pix.fill(green)
            pix[i] = blue
            pix.write()
            time.sleep(0.15)

        for i in range(PIX_SIZE-2,0,-1):
            pix.fill(green)
            pix[i] = red
            pix.write()
            time.sleep(0.15)

        
except KeyboardInterrupt:
    pix.fill(off)
    pix.write()
    time.sleep(0.1)