from machine import Pin
from utime import sleep
from dht import DHT11

DATA_PIN = 18
BTN_PIN = 22

btn_old = 1
btn_new = 1
unit_C = True

datapin = Pin(DATA_PIN, Pin.OUT, Pin.PULL_DOWN)
button = Pin(BTN_PIN, Pin.IN, Pin.PULL_UP)
sensor = DHT11(datapin)
sleep(1)

print("Sensor data:")
while True:
    try:
        btn_new = button.value()
        sensor.measure()
        if btn_new is 0 and btn_old is 1:
            unit_C ^= True

        temp = sensor.temperature()
        if not unit_C:
            temp = int(temp *9/5 + 32)
        hum = sensor.humidity()
        print(f"\rtemperature: {temp} {"C" if unit_C else "F"}\t humidity: {hum} %", end="")
        sleep(.3)
    except KeyboardInterrupt:
        print('bye')
        break