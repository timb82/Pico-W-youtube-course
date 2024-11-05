# type: ignore   // for Pylance & ruff to ignore assembly
# ruff: noqa
import rp2
from machine import Pin

PIN1 = 16
SW1 = 10

pin_sw1 = Pin(SW1, Pin.OUT, Pin.PULL_DOWN)
pin_sw2 = Pin(SW1 + 1, Pin.OUT, Pin.PULL_DOWN)


@rp2.asm_pio(out_init=(rp2.PIO.OUT_LOW,) * 4, out_shiftdir=1)
def bin_counter():
    set(osr, 0b0000)
    mov(pins, osr)
    wrap_target()

    # loop while waiting for button press
    label("read_again")
    mov(isr, null)
    in_(pins, 2)
    nop()[31]
    nop()[31]
    mov(x, isr)
    jmp(not_x, "read_again")

    # red button // bin counter +1
    set(y, 0b0010)
    jmp(x_not_y, "check_green")
    wait(0, pin, 1)
    # x + 1 == !(!x-1)
    mov(x, invert(osr))
    jmp(x_dec, "set_pins")

    # green button // reset
    label("check_green")
    set(y, 0b0001)
    jmp(x_not_y, "read_again")
    wait(0, pin, 0)
    # x = 0  == !x = 0b1111
    set(x, 0b1111)

    label("set_pins")
    mov(osr, invert(x))
    mov(pins, osr)
    wrap()


sm0 = rp2.StateMachine(0, bin_counter, freq=0, out_base=Pin(PIN1), in_base=pin_sw1)
sm0.active(1)

# required for keeping SM alive in vs code, can be omitted when using Thonny
while True:
    pass
