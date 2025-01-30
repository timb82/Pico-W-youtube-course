from rp2 import PIO, asm_pio, StateMachine
from machine import Pin
from time import sleep_ms as sleep

NUM_LEDS = 8
my_color = [0] * NUM_LEDS
my_colors = [
    [64, 154, 255],
    [128, 0, 128],
    [50, 150, 50],
    [255, 30, 30],
    [0, 128, 255],
    [99, 199, 0],
    [128, 128, 128],
    [255, 100, 0],
]


@asm_pio(sideset_init=PIO.OUT_HIGH, out_shiftdir=0, autopull=True, pull_thresh=24)
def ws2812():
    wrap_target()
    label("bit_loop")
    out(x, 1).side(0)
    jmp(not_x, "do_zero").side(1)
    # do one
    nop().side(1)[5 - 1]
    nop().side(0)[2 - 1]
    jmp("bit_loop").side(0)
    label("do_zero")
    nop().side(1)[2 - 1]
    nop().side(0)[5 - 1]
    jmp("bit_loop").side(0)
    wrap()


sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(0))
sm.active(1)


def write_np(data):
    for color in data:
        grb = color[1] << 16 | color[0] << 8 | color[2]
        sm.put(grb, 8)


# while True:
#     pass
