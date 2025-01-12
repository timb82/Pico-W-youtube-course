from machine import Pin
from time import sleep_us
import rp2

PIN_SRVO = 16
FREQ = 2_000_000

servo = Pin(PIN_SRVO, Pin.OUT)


@rp2.asm_pio(
    set_init=rp2.PIO.OUT_LOW, out_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_RIGHT
)
def servo_set():
    wrap_target()
    set(pins, 1)
    wrap()


sm0 = rp2.StateMachine(0, servo_set, freq=FREQ, set_base=servo, out_base=servo)
sm0.active(1)


# Example in python
# servo = Pin(PIN_SRVO, Pin.OUT)

while True:
    pass
    # angle = 180
    # pw = int(angle * 2000 / 180 + 500)
    # servo.on()
    # sleep_us(pw)
    # servo.off()
    # sleep_us(20_000 - pw)
