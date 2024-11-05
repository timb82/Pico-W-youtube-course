import time
import rp2
from machine import Pin

PIN1 = 16
BTN_PIN = 10

@rp2.asm_pio(out_init=(rp2.PIO.OUT_LOW,)*4, out_shiftdir=1)
def wait_pin_low():
    set(x, 0b00000)
    wrap_target()
    # wait(polarity=1, src=, index=) 
    # Polarity: waiting for 0 or 1
    # Looking at src for polarity gpio, pin, irq. GPIO refers to absolute pin no,  pin to in_base & index
    # index of in_base

    # wait(1,gpio,10)        # the same as below, reference through gpio
    wait (1, pin, 0)     # the same as above, reference through in_base
    nop() [31]
    nop() [31]
    mov(x, invert(x))
    mov(pins, x)
    
    wait(0, pin, 0)
    nop() [31]
    nop() [31]
    wrap()

sm0 = rp2.StateMachine(0, 
                       wait_pin_low, 
                       freq=2000, 
                       out_base=Pin(PIN1), 
                       in_base=Pin(BTN_PIN, Pin.IN, Pin.PULL_DOWN),
                       )

sm0.active(1)

while True:
    pass