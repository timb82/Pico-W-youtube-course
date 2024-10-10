from machine import Pin
from utime import sleep
from dht import DHT11
from lcd1602 import LCD

DATA_PIN = 18
BTN_PIN = 22

btn_old = 1
btn_new = 1
unit_C = True

datapin = Pin(DATA_PIN, Pin.OUT, Pin.PULL_DOWN)
button = Pin(BTN_PIN, Pin.IN, Pin.PULL_UP)
sensor = DHT11(datapin)
sleep(1)
lcd = LCD()

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
        lcd.clear()
        print(f"\rtemperature: {temp} {"C" if unit_C else "F"}\t humidity: {hum} %", end="")
        lcd.write(0,0, f"Temp: {temp} {chr(223)}{"C" if unit_C else "F"}")
        lcd.write(0,1, f"Hum:  {hum} %")
        btn_old = button.value()
        sleep(.3)
    except KeyboardInterrupt:
        print('\nbye')
        lcd.clear()
        sleep(0.05)
        lcd.write(6,0, "BYE!")
        sleep(0.3)
        lcd.clear()
        break