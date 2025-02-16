from rp2 import PIO, asm_pio, StateMachine
from machine import Pin
from time import sleep_ms as sleep

TRIG_PIN = 16
ECHO_PIN= 17

@asm_pio(set_init=PIO.OUT_LOW)
def pulse():
    wrap_target()
    nop()
    trap()

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

sm = StateMachine(0, pulse, freq=1_000_000, set_base=trig, in_base=echo)


