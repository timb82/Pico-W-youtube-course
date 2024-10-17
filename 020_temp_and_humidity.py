from machine import Pin
from utime import sleep
from dht import DHT11

DATA_PIN =  18

datapin = Pin(DATA_PIN, Pin.OUT, Pin.PULL_DOWN)

sensor = DHT11(datapin)
sleep(1)

print("Sensor data:")
while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print(f"\rtemperature: {temp}C\t humidity: {hum}%", end="")
        sleep(1)
    except KeyboardInterrupt:
        print('bye')
        break