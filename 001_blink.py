from machine import Pin
from utime import sleep

pin = Pin("LED", Pin.OUT)

print("Starting onboard LED blink")

while True:
    try:
        pin.toggle()
        sleep(0.8)
    except KeyboardInterrupt:
        break
pin.off()
print("Program ended.")
