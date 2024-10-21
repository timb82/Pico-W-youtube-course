from machine import I2C, Pin
from time import sleep, ticks_ms
from imu import MPU6050
from ssd1306 import SSD1306_I2C

I2C_SDA_PIN = 6
I2C_SCL_PIN = 7
I2C_CHN = 1


# i2c_imu = I2C(IMU_I2C_CHN, sda=Pin(IMU_SDA_PIN), scl=Pin(IMU_SCL_PIN), freq=400000)
i2c = I2C(id=I2C_CHN, sda=I2C_SDA_PIN, scl=I2C_SCL_PIN, freq=400000)

mpu = MPU6050(i2c)
dsp = SSD1306_I2C(128, 64, i2c)

dsp.fill(0)
dsp.show()

while True:
    dropped = False
    dsp.text("Uwaga!", 40, 20)
    dsp.text("Gotowy na zrzut", 5, 40)
    dsp.show()
    dsp.fill(0)
    az = round(mpu.accel.z, 3)
    t_start = ticks_ms()
    while az <= 0.92:
        dropped = True
        az = mpu.accel.z
    t_stop = ticks_ms()
    t_drop = t_stop - t_start
    if dropped:
        height = round(16 * (t_drop * 1e-3) ** 2 * 12 * 2.54, 1)
        dsp.text(f"Zrzut!!", 40, 10)
        # dsp.text(f"t_drop = {t_drop} ms", 0, 25)
        dsp.text("wysokosc:", 30, 26)
        dsp.line(79, 29, 83, 26, 1)
        dsp.line(88, 29, 91, 26, 1)
        dsp.text(f"{height:3.1f} cm", 35, 45)
        dsp.show()
        dsp.fill(0)
        sleep(5)
        dropped = False
