from machine import I2C
from utime import ticks_ms
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
conf = 0.01

# calibration coefficients
error_pitch = 0
error_roll = 0
x_offset = 0.0172493133544921875
y_offset = -1.535597393798828125
z_offset = 0.7726116862487792968750
xa_offset = 1.3
ya_offset = -0.25

while True:
    t_start = ticks_ms()
    gx = mpu.gyro.x - x_offset
    gy = -mpu.gyro.y - y_offset
    gz = mpu.gyro.z
    ax = mpu.accel.x
    ay = mpu.accel.y
    az = mpu.accel.z
    pitchG = pitchG + gx * dt
    rollG = rollG + gy * dt
    yawG = yawG + gz * dt
    if az != 0:
        rollA = atan(ax / az) / 2 / pi * 360 - xa_offset
        pitchA = atan(ay / az) / 2 / pi * 360 -ya_offset
        roll_comp = rollA * conf + (1 - conf) * (roll_comp + gy * dt) + error_roll * 0.005
        pitch_comp = pitchA * conf + (1 - conf) * (pitch_comp + gx * dt) + error_pitch * 0.005
        error_pitch = error_pitch + (pitchA - pitch_comp) * dt
        error_roll = error_roll + (rollA - roll_comp) * dt
    cntr += 1
    if cntr == 10:
        print(f"RA={rollA}, PA={pitchA}, Rc={roll_comp}, Pc={pitch_comp}")
#         print(f"RA={rollA}, PA={pitchA}")
#         print(f"Rc={roll_comp}, Pc={pitch_comp}")
        cntr = 0
    t_stop = ticks_ms()
    dt = (t_stop - t_start) / 1000
