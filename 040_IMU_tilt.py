from machine import I2C
from utime import sleep_ms
from imu import MPU6050
from math import atan, pi

I2C_SDA_PIN = 6
I2C_SCL_PIN = 7
I2C_I2C_CHN = 1


# i2c_imu = I2C(IMU_I2C_CHN, sda=Pin(IMU_SDA_PIN), scl=Pin(IMU_SCL_PIN), freq=400000)
i2c = I2C(id=I2C_I2C_CHN, sda=I2C_SDA_PIN, scl=I2C_SCL_PIN)

mpu = MPU6050(i2c)

while True:
    ax = mpu.accel.x
    ay = mpu.accel.y
    az = mpu.accel.z
    if ax > 1:
        ax = 1
    elif ax < -1:
        ax = -1
    if ay > 1:
        ay = 1
    elif ay < -1:
        ay = -1
    if az > 1:
        az = 1
    elif az < -1:
        az = -1
    pitch = atan(ay / az) / 2 / pi * 360
    roll = atan(ax / az) / 2 / pi * 360
    # print(f"X={ax:+0.8f} g \tY={ay:+0.8f} g \tZ={az:+0.8f} g")
    print(f"tilt angle: \tX={roll: .2f} \tY={pitch: .2f}\t\tdeg")
    sleep_ms(200)
