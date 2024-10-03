from machine import ADC
from utime import sleep


POTPIN = 28
pot = ADC(POTPIN)
sensor_temp = ADC(4)

temperature = 27 - (sensor_temp.read_u16() * 3.3 / 65535 - 0.706) / 0.001721
print(f"Temperature reading: {temperature}\nStarting ADC callibration.\n")

input("Turn the potentiometer to MINIMUM, type anything and press Enter...")
print("acquiring samples")

low = []
high = []

for i in range(15000):
    low.append(pot.read_u16())
    # sleep(0.001)

input("Turn the potentiometer to MAXIMUM, type anything and press Enter...")
print("acquiring samples")

for i in range(15000):
    high.append(pot.read_u16())
    # sleep(0.001)

x1 = 0
y1 = round(sum(low) / len(low))
x2 = 2**16 - 1
y2 = round(sum(high) / len(high)) - y1
a = (y1 + y2) / (x1 + x2)
b = a * x1 - y1

print(f"Low:\nmin: {min(low)},\tavg:{y1}\n")
print(f"High:\nmax: {max(high)},\tavg:{y2}\n")

while True:
    try:
        A = 3.3
        val = round(A / y2 * (pot.read_u16() - y1), 3)
        if val > 3.3:
            val = 3.3
        if val < 0:
            val = 0
        print(val)
        sleep(0.25)
    except KeyboardInterrupt:
        print(f"y1 = \t{y1}\ny2 = \t{y2}")
        print(f"A / {y2} * (pot.read_u16() - {y1})")
        break
