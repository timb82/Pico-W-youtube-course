from machine import Pin
import time
import rp2

PIN1=16
PIN2=PIN1+1
PIN3=PIN1+2
PIN4=PIN1+3


@rp2.asm_pio(out_init=(rp2.PIO.OUT_LOW,)*4, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def pio_prg():
    wrap_target()
    pull()
    mov(x,osr)
    mov(pins, x)
    mov(isr, x)
    push()
    wrap()

sm0 = rp2.StateMachine(0, pio_prg, freq=2000, out_base=Pin(PIN1))
sm0.active(True)
for i in range(17):
    sm0.put(i)
    print(sm0.get())
    time.sleep(0.3)

time.sleep(2)
sm0.active(False)



# led1=Pin(PIN1,Pin.OUT)
# led2=Pin(PIN2,Pin.OUT)
# led3=Pin(PIN3,Pin.OUT)
# led4=Pin(PIN4,Pin.OUT)

# leds = [led1, led2, led3, led4]

# for l in leds:
#     l.on()

# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     for l in leds:
#         l.off()