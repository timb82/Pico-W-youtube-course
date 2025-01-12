from rp2 import PIO, StateMachine, asm_pio
from machine import Pin
from time import sleep, ticks_ms

led = Pin(16, Pin.OUT)

# # Flash five times just to prove LED works
# for n in range(10):
#     led.toggle()
#     sleep(0.125)


@asm_pio(set_init=PIO.OUT_LOW, out_init=PIO.OUT_LOW)
def LedFlash():
    # USE_MOV = False
    # pull(block)  # OSR = Pull()
    wrap_target()
    set(osr, 2000000)
    mov(x, osr)  # X = OSR
    label("main_loop")  # while True:
    jmp("on")  #   on(X)
    label("on_rts")  #
    # push(block)  #   push(ISR)
    jmp("off")  #   off(X)
    label("off_rts")  #
    # push(block)  #   push(ISR)
    jmp("main_loop")  #

    label("on")  # def on(X):
    # if USE_MOV:  #   led = 1
    #     set(y, 1)
    #     mov(pins, y)
    # else:
    set(pins, 1)
    mov(y, x)  #   Y = X
    label("on_loop")  #   wait for Y-- == 0:
    jmp(y_dec, "on_loop")  #
    jmp("on_rts")  #   return

    label("off")  # def off(X):
    # if USE_MOV:  #   led = 0
    #     set(y, 0)
    #     mov(pins, y)
    # else:
    set(pins, 0)
    mov(y, x)  #   Y = X
    label("off_loop")  #   wait for Y-- == 0:
    jmp(y_dec, "off_loop")  #
    jmp("off_rts")  #   return
    wrap()


hz = 2_000_000

# # Force the pin to be enabled if we forgot to put 'set_init=' in
# # the '@asm_pio()'

# if LedFlash[-2] == None:
#     LedFlash[-2] = [PIO.OUT_LOW]

# # And force it to be enabled if using 'mov(pins, x)' and we forgot
# # to include 'out_init=' in the '@asm_pio'.

# if LedFlash[-3] == None:
#     LedFlash[-3] = [PIO.OUT_LOW]

sm = StateMachine(0, LedFlash, freq=hz, set_base=led, out_base=led)
sm.active(1)

# sm.put(int(hz / 2))
while True:
    pass
#     sm.get()
#     print("Tick {}".format(ticks_ms() / 1000))
