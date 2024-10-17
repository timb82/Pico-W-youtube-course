from lcd1602 import LCD

lcd = LCD()

while True:
    try:
        name = input("What is your name? ")
        lcd.clear()
        lcd.write(0,0, "Hi "+name)
        lcd.write(0,1, "Welcome to Pico!")
    except KeyboardInterrupt:
        lcd.clear()
        break