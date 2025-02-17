from rp2 import PIO, asm_pio, StateMachine
from machine import Pin
from time import sleep

TRIG_PIN = 16
ECHO_PIN = 17


@asm_pio(set_init=PIO.OUT_LOW)
def pulse():
    wrap_target()
    pull(block)
    mov(x, osr)
    set(pins, 1)[10 - 1]
    set(pins, 0)
    wait(1, pin, 0)
    label("loop")
    mov(y, pins)  # 1st clock cycle
    jmp(not_y, "break_loop")  # 2nd clock cycle
    jmp(x_dec, "loop")  # 3rd clock cycle
    label("break_loop")
    mov(isr, invert(x))
    push()
    wrap()


trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

sm = StateMachine(0, pulse, freq=1_000_000, set_base=trig, in_base=echo)
sm.active(1)

while True:
    sm.put(0xFFFFFFFF)
    print("pulse launched")
    clock_cycles = sm.get() * 3 / 2
    dist = clock_cycles * 0.03444
    print(f"distance to target: {dist}")
    sleep(0.25)
