from machine import I2C
from time import sleep_ms, ticks_ms
from imu import MPU6050
from math import atan, pi
# from ssd1306 import SSD1306_I2C

OLED_SDA_PIN = 6
OLED_SCL_PIN = 7
OLED_I2C_CHN = 1

i2c = I2C(id=OLED_I2C_CHN, sda=OLED_SDA_PIN, scl=OLED_SCL_PIN, freq=400000)
mpu = MPU6050(i2c)

pitchG = 0
rollG = 0
roll_comp = 0
pitch_comp = 0
# yawG = 0
dt = 0
cntr = 0
conf = 0.1

while True:
    t_start = ticks_ms()
    gx = mpu.gyro.x  - 0.05022978
    gy = -mpu.gyro.y  + 1.5604778
    # gz = mpu.gyro.z - 0.799  # 0.8015522
    ax = mpu.accel.x
    ay = mpu.accel.y
    az = mpu.accel.z
    rollG = rollG + gy * dt
    pitchG = pitchG + gx * dt
    # yawG = yawG + gz * dt
    if az!=0:
        rollA = atan(ax / az) / 2 / pi * 360
        pitchA = atan(ay / az) / 2 / pi * 360
        roll_comp = rollA * conf + (1-conf) * (roll_comp + gy*dt)
        pitch_comp = pitchA * conf + (1-conf) * (pitch_comp + gx*dt)
    cntr += 1
    if cntr == 10:
        print(f"RG={rollG}, PG={pitchG}, Rc={roll_comp}, Pc={pitch_comp}")
        cntr = 0
    t_stop = ticks_ms()
    dt = (t_stop - t_start) / 1000
