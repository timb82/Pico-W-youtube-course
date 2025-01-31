from rp2 import PIO, asm_pio, StateMachine
from machine import Pin
from time import sleep_ms as sleep

PIN_NUM = 0
NUM_LEDS = 8
BRIGHTNESS = 0.05
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


@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=0, autopull=True, pull_thresh=24)
def ws2812():
    # T1 = 2
    # T2 = 5
    # T3 = 3
    # wrap_target()
    # label("bitloop")
    # out(x, 1).side(0)[T3 - 1]
    # jmp(not_x, "do_zero").side(1)[T1 - 1]
    # jmp("bitloop").side(1)[T2 - 1]
    # label("do_zero")
    # nop().side(0)[T2 - 1]
    # wrap()

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


sm = StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))
sm.active(1)


def write_np(data):
    for color in data:
        grb = color[1] << 16 | color[0] << 8 | color[2]
        sm.put(grb, 8)


def dim(colors, brightness):
    new_cols = []
    for i in range(len(colors)):
        new_cols.append([int(colors[i][j] * brightness) for j in range(len(colors[i]))])
    return new_cols


def color_wheel(pos):
    if pos < 0 or pos > 255:
        return [0, 0, 0]
    if pos < 85:
        return [255 - pos * 3, pos * 3, 0]
    if pos < 170:
        pos -= 85
        return [0, 255 - pos * 3, pos * 3]
    pos -= 170
    return [pos * 3, 0, 255 - pos * 3]


def rainbow():
    for i in range(256):
        for p in range(NUM_LEDS):
            color = (p * 256 // NUM_LEDS) + i
            my_colors[p] = color_wheel(color & 0xFF)

        write_np(dim(my_colors, BRIGHTNESS))
        sleep(5)


while True:
    rainbow()
# while True:
#     pass
