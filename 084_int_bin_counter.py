from machine import Pin
from time import ticks_ms

BTN_PIN = 27
R_PIN = 13
G_PIN = 14
B_PIN = 15

led_r = Pin(R_PIN, Pin.OUT)
led_g = Pin(G_PIN, Pin.OUT)
led_b = Pin(B_PIN, Pin.OUT)

debounce = 20
press = 0
p_time_old = 0


def btn_int(pin):
    global press, p_time_old
    p_time = ticks_ms()
    if p_time - p_time_old > debounce and pin.irq().flags() == Pin.IRQ_FALLING:
        press += 1
        if press > 7:
            press = 0
        print("triggered", press)

        led_r.toggle()
    p_time_old = p_time


def toggle_leds(pin):
    if pin is led_r:
        led_g.toggle()
    if pin is led_g:
        led_b.toggle()


btn = Pin(BTN_PIN, Pin.IN, Pin.PULL_UP)


btn.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=btn_int)
led_r.irq(trigger=Pin.IRQ_FALLING, handler=toggle_leds)
led_g.irq(trigger=Pin.IRQ_FALLING, handler=toggle_leds)

try:
    while True:
        pass

except KeyboardInterrupt:
    led_r.irq(handler=None)
    led_g.irq(handler=None)
    led_b.irq(handler=None)
    led_r.off()
    led_g.off()
    led_b.off()
