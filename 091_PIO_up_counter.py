from machine import Pin
import rp2

PIN1=16

@rp2.asm_pio(out_init=(rp2.PIO.OUT_LOW,)*4, out_shiftdir=1)
def counter():
    wrap_target()
    set(x, 0b1111)
    label("loop")
    set(y, 0b11111)
    mov(pins, invert(x)) 
    label('delay')
    nop() [31]
    jmp(y_dec, 'delay')[31]
    jmp(x_dec, 'loop')

    wrap()


sm0 = rp2.StateMachine(0,counter, freq=2000, out_base=Pin(PIN1))
sm0.active(1)


while True:
    pass