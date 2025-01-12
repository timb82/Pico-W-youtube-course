from machine import Pin
from time import sleep_us
from rp2 import PIO, asm_pio, StateMachine

PIN_SRVO = 20
FREQ = 2_000_000

servo = Pin(PIN_SRVO, Pin.OUT)


@asm_pio(set_init=PIO.OUT_LOW, out_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_RIGHT)
def servo_set():
    # set pulse width of 1500ms to osr
    # set(x, 0b10111)
    # in_(x, 5)
    # set(x, 0b01110)
    # in_(x, 5)
    # set(x, 0b00000)
    # in_(x, 1)
    # mov(osr, isr)

    # set pulse width of 500ms to osr
    set(x, 0b11111)
    in_(x, 5)
    set(x, 0b0100)
    in_(x, 4)
    mov(osr, isr)

    # set period of 20_000ms to isr
    mov(isr, null)
    set(y, 0b10011)
    in_(y, 5)
    set(y, 0b10001)
    in_(y, 5)
    set(y, 0b00000)
    in_(y, 5)

    wrap_target()
    mov(x, osr)
    mov(y, isr)
    set(pins, 0)

    label("time loop")  # 1ms loop @ freq=2MHz
    jmp(x_not_y, "next")
    set(pins, 1)
    label("next")
    jmp(y_dec, "time loop")
    wrap()


sm0 = StateMachine(0, servo_set, freq=FREQ, set_base=servo, out_base=servo)
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
