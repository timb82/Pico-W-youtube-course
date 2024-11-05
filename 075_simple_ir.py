from machine import Pin
from ir_rx.nec import NEC_8
from ir_rx.print_error import print_error
from time import sleep

IR_PIN = 17
R_PIN = 13
G_PIN = 14
B_PIN = 15

led_r = Pin(R_PIN, Pin.OUT)
led_g = Pin(G_PIN, Pin.OUT)
led_b = Pin(B_PIN, Pin.OUT)

# codes = {1: 69, 2: 70, 3: 71, 4: 68, 5: 64}
codes = {
    69: 1,
    70: 2,
    71: 3,
    68: 4,
    64: 5,
    67: 6,
    7: 7,
    21: 8,
    9: 9,
    25: 0,
    22: "*",
    13: "#",
    24: "up",
    82: "down",
    8: "left",
    90: "right",
    28: "OK",
}


def cb(data, _a, _b):
    if data in codes.keys():
        print(codes[data])
        if codes[data] == 1:
            led_b.toggle()
        if codes[data] == 2:
            led_g.toggle()
        if codes[data] == 3:
            led_r.toggle()
    elif data != -1:
        print(data)


ir = NEC_8(Pin(IR_PIN, Pin.IN), cb)

try:
    while True:
        sleep(0.01)
except KeyboardInterrupt:
    ir.close()
    led_r.off()
    led_g.off()
    led_b.off()
    print("bye")
