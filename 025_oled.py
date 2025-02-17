from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from utime import sleep

SDA = 14
SCL = 15

# using default address 0x3C
i2c = I2C(id=1, sda=Pin(SDA), scl=Pin(SCL))
display = SSD1306_I2C(128, 64, i2c)
display.rect(0, 0, 128, 64, 1, True)
display.text("Hej Ewka!!!", 5, 10, 0)
display.text("Halo Marta!!!", 5, 30, 0)
display.invert(1)

display.show()

# sleep(1.5)
# display.poweroff()
# sleep(1.5)
# display.poweron()
# display.show()


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
