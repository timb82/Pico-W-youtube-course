import time
import rp2
from machine import Pin

PIN1 = 16
SW1 = 10
SW2 = 11

pin10 = Pin(SW1, Pin.IN, Pin.PULL_DOWN)
pin11 = Pin(SW2, Pin.IN, Pin.PULL_DOWN)


@rp2.asm_pio(out_init=(rp2.PIO.OUT_LOW,) * 4, out_shiftdir=1)
def btn_watch():
    wrap_target()
    label("read_again")
    mov(isr, null)
    in_(pins, 2)
    nop()[31]
    nop()[31]
    mov(x, isr)
    # not_x : jumps if there's nothing in x. If x=0 -> jump
    # not_y : jumps if there's nothing in y. If y=0 -> jump
    # x_not_y : jumps if x is not equal to y
    # x_dec : jumps if x is not 0, then decrement x by 1
    # pin : jump if pin is not zero
    # not_osre : jump if osr is empty
    jmp(not_x, "read_again")
    set(y, 0b0001)
    jmp(x_not_y, "check_green")
    set(y, 0b0101)
    mov(pins, y)
    label("check_green")
    set(y, 0b0010)
    jmp(x_not_y, "read_again")
    set(y, 0b1010)
    mov(pins, y)
    wrap()


sm0 = rp2.StateMachine(0, btn_watch, freq=2000, out_base=Pin(PIN1), in_base=pin10)


sm0.active(1)

while True:
    pass
