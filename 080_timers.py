from machine import Pin, Timer

#led pins
R_PIN = 13
G_PIN = 14
B_PIN = 15

led_r = Pin (R_PIN, Pin.OUT)

def r_blink(Source):
    led_r.toggle()

timer_r = Timer(period=100, mode=Timer.PERIODIC, callback=r_blink)

while True:
    pass
