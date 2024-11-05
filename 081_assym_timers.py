from machine import Pin, Timer
from time import sleep
#led pins
R_PIN = 13
G_PIN = 14
B_PIN = 15

led_r = Pin (R_PIN, Pin.OUT)
led_g = Pin (G_PIN, Pin.OUT)
led_b = Pin (B_PIN, Pin.OUT)

def turn_red_off(Source):
    led_r.off()

def turn_green_off(Source):
    led_g.off()

def r_blink(Source):
    led_r.on()
    red_off = Timer(period=100, mode=Timer.ONE_SHOT, callback=turn_red_off)

def g_blink(Source):
    led_g.on()
    Timer(period = 800, mode=Timer.ONE_SHOT, callback=turn_green_off)

def b_blink(Source):
    led_b.toggle()


timer_r = Timer(period=2000, mode=Timer.PERIODIC, callback=r_blink)
timer_g = Timer(period=1500, mode=Timer.PERIODIC, callback=g_blink)
# timer_b  = Timer(period=3000, mode=Timer.PERIODIC, callback=b_blink)

x=0
try:
    while True:
        print(x)
        sleep(1)
        x+=1

except KeyboardInterrupt:
    timer_r.deinit()
    timer_g.deinit()
    # timer_b.deinit()
    led_r.off()
    led_g.off()
    led_b.off()