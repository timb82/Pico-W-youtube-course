import time
import rp2
from machine import Pin

PIN1 = 16
BTN_PIN = 10

@rp2.asm_pio(out_init=(rp2.PIO.OUT_LOW,)*4, out_shiftdir=1)
def bin_counter():
    wrap_target()
    set (x, 0b1111)
    label('loop')
    mov(pins, invert(x))
    wait (1, pin, 0)
    nop() [31]
    nop() [31]
    wait(0, pin, 0)
    nop() [31]
    nop() [31]
    jmp(x_dec, 'loop')
    wrap()

sm0 = rp2.StateMachine(0, 
                       bin_counter, 
                       freq=2000, 
                       out_base=Pin(PIN1), 
                       in_base=Pin(BTN_PIN, Pin.IN, Pin.PULL_DOWN),
                       )

sm0.active(1)

while True:
    pass