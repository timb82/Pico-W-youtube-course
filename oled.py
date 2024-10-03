from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

# using default address 0x3C
i2c = I2C(id=0, sda=Pin(4), scl=Pin(5))
display = SSD1306_I2C(128, 64, i2c)

display.text("\nHello, World!", 0, 0, 1)
display.show()
