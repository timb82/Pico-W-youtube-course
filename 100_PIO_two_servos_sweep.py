from machine import Pin
from time import sleep_us
from rp2 import PIO, asm_pio, StateMachine

PIN_SRVO1 = 20
PIN_SRVO2 = 21
FREQ = 2_000_000
PERIOD = 19_999  # us

delay = 3_000

# servo = Pin(PIN_SRVO1, Pin.OUT)
# servo2 = Pin(PIN_SRVO2, Pin.OUT)


@asm_pio(set_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_RIGHT)
def servo_set():
    wrap_target()
    mov(x, osr)
    mov(y, isr)
    set(pins, 0)

    label("time_loop")  # 1ms loop @ freq=2MHz
    jmp(x_not_y, "next")
    set(pins, 1)
    nop()
    label("next")
    jmp(y_dec, "time_loop")
    wrap()


def d2pw(angle):
    return int(angle * 2000 / 180 + 500)


try:
    sm0 = StateMachine(1, servo_set, freq=FREQ, set_base=Pin(PIN_SRVO1))
    sm0.active(0)
    sm0.put(PERIOD)
    sm0.exec("pull()")
    sm0.exec("mov(isr, osr)")

    sm1 = StateMachine(4, servo_set, freq=FREQ, set_base=Pin(PIN_SRVO2))
    sm1.active(0)
    sm1.put(PERIOD)
    sm1.exec("pull()")
    sm1.exec("mov(isr, osr)")
    sm0.put(d2pw(0))
    sm0.exec("pull()")
    sm1.put(d2pw(180))
    sm1.exec("pull()")

    sleep_us(300_000)
    sm0.active(1)
    sm1.active(1)
    z = True
    while z is True:
        for i in range(0, 180, 1):
            sm0.put(d2pw(i))
            sm1.put(d2pw(180 - i))
            sm0.exec("pull()")
            sm1.exec("pull()")
            sleep_us(delay)
        for i in range(180, 0, -1):
            sm0.put(d2pw(i))
            sm1.put(d2pw(180 - i))
            sm0.exec("pull()")
            sm1.exec("pull()")
            sleep_us(delay)
        sleep_us(10 * delay)
        z = False

except KeyboardInterrupt:
    sm0.active(0)
    sm1.active(0)
    sleep_us(delay)
    sm0.put(d2pw(0))
    sm0.exec("pull()")
    sm0.active(1)
    sm1.put(d2pw(180))
    sm1.exec("pull()")
    sm1.active(1)
    sleep_us(1_000_000)
    # sm0.active(0)
    # sm1.active(0)
