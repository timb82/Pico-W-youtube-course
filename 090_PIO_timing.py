from machine import Pin
import time
import rp2

PIN1 = 16

@rp2.asm_pio(out_init=(rp2.PIO.OUT_LOW,)*4, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
# def pio_prog():
#     wrap_target()
#     pull()
#     set(y, 0b0001)
#     mov(x, osr)       
#     mov(isr, x)
#     in_(y,1)
#     mov(pins, isr)
#     push()
#     wrap()

def pio_prog():
    wrap_target()
    set(x,0b1111) [31]
    label('bitloop')
    mov(pins, x) [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    jmp(x_dec,'bitloop') [31]
    wrap()

sm0 = rp2.StateMachine(0, pio_prog, freq=2000, out_base=(Pin(PIN1)))
sm0.active(True)
while True:
    pass
#     x = int(input("enter your number: "))
#     sm0.put(x)
#     x = sm0.get()
#     print("doubled value: ", x)