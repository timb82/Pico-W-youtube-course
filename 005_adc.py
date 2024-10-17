import machine
from time import sleep

POTPIN = 28

myPot = machine.ADC(POTPIN)

while True:
    val = myPot.read_u16()  # / 65535 * 3.3
    voltage = 3.3 * (val - 300) / (65535 - 300)
    if voltage < 0:
        voltage = 0
    print(voltage)
    sleep(0.25)
