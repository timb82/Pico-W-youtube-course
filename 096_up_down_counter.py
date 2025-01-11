from machine import Pin
import rp2

PIN1 = 16
SW1 = 10
SW2 = 11

pin_sw1 = Pin(SW1, Pin.IN, Pin.PULL_DOWN)


@rp2.asm_pio(out_init=(rp2.PIO.OUT_LOW,) * 4, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def inc_dec():
    set(y, 0b0000)
    wrap_target()

    # read button input
    label("btn_read")
    mov(isr, null)
    in_(pins, 2)
    mov(x, isr)
    jmp(not_x, "btn_read")
    # move main counter from y to osr
    mov(osr, y)
    set(y, 0b0010)
    jmp(x_not_y, "inc")

    # decrement here
    wait(0, pin, 1)
    mov(y, osr)
    jmp(y_dec, "next")
    label("next")
    mov(pins, y)
    jmp("btn_read")

    # increment here
    label("inc")
    wait(0, pin, 0)
    mov(y, invert(osr))
    jmp(y_dec, "next2")
    label("next2")
    mov(y, invert(y))
    mov(pins, y)
    jmp("btn_read")

    wrap()


sm0 = rp2.StateMachine(0, inc_dec, freq=0, out_base=Pin(PIN1), in_base=pin_sw1)
sm0.active(1)


while True:
    pass
