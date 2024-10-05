from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

# using default address 0x3C
i2c = I2C(id=0, sda=Pin(4), scl=Pin(5))
display = SSD1306_I2C(128, 64, i2c)

display.text("Hej Ewka!!!", 0, 10, 1)
display.text("Halo Marta!!!", 0, 30, 1)

display.show()

# # display.fill(0)
# # display.show()
# while True:
#     try:
#         a = 1
#     except KeyboardInterrupt:
#         display.fill(0)
#         display.show()
#         print("end")
#         break
