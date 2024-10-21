from machine import I2C, Pin
from time import sleep, ticks_ms
from imu import MPU6050
from ssd1306 import SSD1306_I2C
from math import atan, pi

I2C_SDA_PIN = 6
I2C_SCL_PIN = 7
I2C_CHN = 1


# i2c_imu = I2C(IMU_I2C_CHN, sda=Pin(IMU_SDA_PIN), scl=Pin(IMU_SCL_PIN), freq=400000)
i2c = I2C(id=I2C_CHN, sda=I2C_SDA_PIN, scl=I2C_SCL_PIN, freq=400000)

mpu = MPU6050(i2c)
dsp = SSD1306_I2C(128, 64, i2c)


def refresh(dx, dy):
    if dx > 45:
        dx = 45
    elif dx < -45:
        dx = -45
    if dy > 45:
        dy = 45
    elif dy < -45:
        dy = -45
    x = int(dx * 64 / 45)
    y = int(dy * 27 / 45)
    dsp.fill(0)
    dsp.hline(2, 38, 124, 1)
    dsp.vline(64, 12, 60, 1)
    dsp.rect(0, 10, 128, 54, 1)
    dsp.ellipse(64 - x, 38 - y, 6, 5, 1, True)
    dsp.ellipse(64 - x + 1, 38 - y - 1, 2, 2, 0, True)
    dsp.pixel(64 - x + 2, 38 - y - 2, 1)
    dsp.text(f"P:{dx:02.0f}", 0, 0, 1)
    dsp.text(f"R:{dy:02.0f}", 92, 0, 1)
    dsp.show()


while True:
    ax = mpu.accel.x
    ay = mpu.accel.y
    az = mpu.accel.z
    A = [ax, ay, az]
    for a in A:
        if a > 1:
            a = 1
        elif a < -1:
            a = -1
    pitch = int(atan(ay / az) / 2 / pi * 360)
    roll = int(atan(ax / az) / 2 / pi * 360)

    refresh(pitch, roll)
