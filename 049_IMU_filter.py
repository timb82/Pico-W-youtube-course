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
yawG = 0
dt = 0
cntr = 0
conf = 0.05

#calibration coefficients
x_offset = 0.0172493133544921875
y_offset = -1.535597393798828125      #-1.530371189117431640625000
z_offset = 0.7726116862487792968750   #0.769709777832031250000000
callibration = False   # Set to True to get callibration coefficients
if callibration:
    t0=ticks_ms()
    cal_time=60

while True:
    try:
        t_start = ticks_ms()
        gx = mpu.gyro.x  - x_offset
        gy = -mpu.gyro.y  - y_offset
        gz = mpu.gyro.z - z_offset
        ax = mpu.accel.x
        ay = mpu.accel.y
        az = mpu.accel.z
        pitchG = pitchG + gx * dt
        rollG = rollG + gy * dt
        yawG = yawG + gz * dt
        if az!=0:
            rollA = atan(ax / az) / 2 / pi * 360
            pitchA = atan(ay / az) / 2 / pi * 360
            roll_comp = rollA * conf + (1-conf) * (roll_comp + gy*dt)
            pitch_comp = pitchA * conf + (1-conf) * (pitch_comp + gx*dt)
        cntr += 1
        if cntr == 10:
            if callibration:
                print(f"x={pitchG}, y={rollG}, z={yawG}")
                if (ticks_ms()-t0)/1000 >cal_time:
                    raise KeyboardInterrupt
            else:
                print(f"RG={rollG}, PG={pitchG}, Rc={roll_comp}, Pc={pitch_comp}, Y={yawG}")
            cntr = 0
        t_stop = ticks_ms()
        dt = (t_stop - t_start) / 1000
    except KeyboardInterrupt:
        if callibration:
            Ax,Ay,Az = pitchG, rollG, yawG
            t = (ticks_ms()-t0)/1000
            print(f"Ellapsed time: {t:.2f}\n callibration values:")
            print(f"x_off = {x_offset + Ax/t: .22f}\ny_off = {y_offset + Ay/t: .22f}\nz_off = {z_offset+ Az/t: .22f}")
            print(f"\n dx = {Ax/t: .22f}\ndy = {Ay/t: .22f}\ndz = {Az/t: .22f}")
        break
