import neopixel
from time import sleep
from machine import Pin

PIX_SIZE = 8
PIX_PIN = 5
pin = Pin(PIX_PIN, Pin.OUT)

def get_RGB(deg, A=1):
    m=1/60
    if deg >=0 and deg<60:
        rgb=[A,0,A*m*deg]
    elif deg>= 60 and deg<120:
        rgb = [A*(1-m*(deg-60)), 0 ,A]
    elif deg>=120 and deg<180:
        rgb = [0, A*m*(deg-120), A]
    elif deg>=180 and deg<240:
        rgb=[0,A,A*(1-m*(deg-180))]
    elif deg >=240 and deg<300:
        rgb= [A*m*(deg-240), A,0]
    elif deg >=300 and deg <360:
        rgb=[A, A*(1-m*(deg-300)),0]
    else:  
        rgb=[0,0,0]
    return [int(val) for val in rgb]


pix = neopixel.NeoPixel(pin, PIX_SIZE)

try:
    while True:
        for d in range (0, 259, 1):
            for p in range(PIX_SIZE):
                pix[p] = get_RGB(d, 3*(p+1))
                pix.write()
            sleep(0.01)
        for d in range (259,1, -1):
            for p in range(PIX_SIZE):
                pix[p] = get_RGB(d, 3*(p+1))
                pix.write()
            sleep(0.01)

except KeyboardInterrupt:
    pix.fill([0,0,0])
    pix.write()
    sleep(0.2)