from rp2 import PIO, asm_pio, StateMachine
from machine import Pin, I2C
from utime import sleep, time
from ssd1306 import SSD1306_I2C
import sys

TRIG_PIN = 16
ECHO_PIN = 17
SDA = 14
SCL = 15
FREQ = 10_000_000


class ERR(Exception):
    def __init__(self, n):
        super().__init__()
        self.n = n
        self.c = 0

    def log(self, error):
        self.c += 1
        if self.c < self.n:
            with open("err.log", "a+") as f:
                f.write(f"{time()}: ")
                sys.print_exception(error, f)
        else:
            machine.soft_reset()  # or whatever you need


err = ERR(100)


@asm_pio(set_init=PIO.OUT_LOW)
def pulse():
    wrap_target()
    pull(block)
    mov(x, osr)
    set(pins, 1)[31]
    nop()[31]
    nop()[31]
    nop()[3]
    set(pins, 0)
    wait(1, pin, 0)
    label("loop")
    in_(pins, 1)  # 1st clock cycle
    mov(y, isr)  # 2nd clock cycle
    jmp(not_y, "break_loop")  # 3rd clock cycle
    jmp(x_dec, "loop")  # 4th clock cycle
    label("break_loop")
    mov(isr, invert(x))
    push()
    wrap()


trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

i2c = I2C(id=1, sda=Pin(SDA), scl=Pin(SCL))
display = SSD1306_I2C(128, 64, i2c)


def dprint(distance):
    display.rect(0, 0, 128, 64, 1, True)
    display.text("Dystans:", 30, 20, 0)
    display.text(f"{distance:.2f} cm", 30, 40, 0)
    display.invert(1)
    display.show()


sm = StateMachine(0, pulse, freq=FREQ, set_base=trig, in_base=echo)
# sm.active(1)

try:
    while True:
        # sm.put(0xFFFFFFFF)
        # print("pulse launched")
        clock_cycles = 1452
        # clock_cycles = sm.get() * 4 / 2  # no of PIO cycles / 2 (forth and back distance)
        dist = clock_cycles * 0.03444 * 1e6 / FREQ
        dprint(dist)
        # print(f"distance to target: {dist}")
        sleep(0.2)
# except KeyboardInterrupt:
#     display.rect(0, 0, 128, 64, 1, True)
#     display.text("BYE!", 40, 40, 0)
#     display.invert(1)
#     display.show()
#     sleep(0.4)
#     display.poweroff()


except BaseException as e:
    err.log(e)
    # import sys

    # print("exception", e)
    # sys.print_exception(e)
    # print("-" * 10)
    # display.rect(0, 0, 128, 64, 1, True)
    # display.text("fuck!", 0, 0, 0)
    # display.text(e, 0, 20, 0)
    # display.invert(1)
    # display.show()
    # sleep(0.4)
