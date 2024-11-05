from machine import Pin
from time import ticks_ms

BTN_PIN = 27
LED_PIN = 13
debounce = 80
press = 0
p_time_old = 0


def btn_int(pin):
    global press, p_time_old
    p_time = ticks_ms()
    if p_time - p_time_old > debounce:
        press += 1
        print("triggered", press)
        led.toggle()
    p_time_old = p_time


btn = Pin(BTN_PIN, Pin.IN, Pin.PULL_UP)
led = Pin(LED_PIN, Pin.OUT)


btn.irq(trigger=Pin.IRQ_FALLING, handler=btn_int)

try:
    while True:
        pass

except KeyboardInterrupt:
    led.off()
