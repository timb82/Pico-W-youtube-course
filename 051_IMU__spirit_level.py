from machine import I2C
from utime import ticks_ms
from imu import MPU6050
from math import atan, pi
from ssd1306 import SSD1306_I2C

I2C_SDA_PIN = 6
I2C_SCL_PIN = 7
I2C_CHN = 1
MAX_ANGLE = 45

i2c = I2C(id=I2C_CHN, sda=I2C_SDA_PIN, scl=I2C_SCL_PIN, freq=400000)
dsp = SSD1306_I2C(128, 64, i2c)
mpu = MPU6050(i2c)

pitchG = 0
rollG = 0
roll_comp = 0
pitch_comp = 0
yawG = 0
dt = 0
cntr = 0
conf = 0.1
err_conf = 0.005

# calibration coefficients
error_pitch = 0
error_roll = 0
x_offset = 0.0172493133544921875
y_offset = -1.535597393798828125
z_offset = 0.7726116862487792968750
xa_offset = 1.3
ya_offset = -0.25


def refresh_disp(phi_x, phi_y):
    if phi_x > MAX_ANGLE:
        phi_x = MAX_ANGLE
    elif phi_x < -MAX_ANGLE:
        phi_x = -MAX_ANGLE
    if phi_y > MAX_ANGLE:
        phi_y = MAX_ANGLE
    elif phi_y < -MAX_ANGLE:
        phi_y = -MAX_ANGLE
    x = int(phi_x * 64 / MAX_ANGLE)
    y = int(phi_y * 27 / MAX_ANGLE)
    dsp.fill(0)
    dsp.hline(2, 38, 124, 1)
    dsp.vline(64, 12, 60, 1)
    dsp.rect(0, 10, 128, 54, 1)
    dsp.ellipse(64 - x, 38 - y, 6, 5, 1, True)
    dsp.ellipse(64 - x + 1, 38 - y - 1, 2, 2, 0, True)
    dsp.pixel(64 - x + 2, 38 - y - 2, 1)
    dsp.text(f"P:{phi_x:02.0f}", 0, 0, 1)
    dsp.text(f"R:{phi_y:02.0f}", 92, 0, 1)
    dsp.show()


def update_P_R():
    global pitchG
    global rollG
    global roll_comp
    global pitch_comp
    global error_pitch
    global error_roll
    global cntr
    global dt
    t_start = ticks_ms()
    gx = mpu.gyro.x - x_offset
    gy = -mpu.gyro.y - y_offset
    ax = mpu.accel.x
    ay = mpu.accel.y
    az = mpu.accel.z
    pitchG = pitchG + gx * dt
    rollG = rollG + gy * dt
    if az != 0:
        rollA = atan(ax / az) / 2 / pi * 360 - xa_offset
        pitchA = atan(ay / az) / 2 / pi * 360 - ya_offset
        roll_comp = (
            rollA * conf + (1 - conf) * (roll_comp + gy * dt) + error_roll * err_conf
        )
        pitch_comp = (
            pitchA * conf + (1 - conf) * (pitch_comp + gx * dt) + error_pitch * err_conf
        )
        error_pitch = error_pitch + (pitchA - pitch_comp) * dt
        error_roll = error_roll + (rollA - roll_comp) * dt
    # cntr += 1
    # if cntr == 10:
    #     print(f"RA={rollA}, PA={pitchA}, Rc={roll_comp}, Pc={pitch_comp}")
    #     #         print(f"RA={rollA}, PA={pitchA}")
    #     #         print(f"Rc={roll_comp}, Pc={pitch_comp}")
    #     cntr = 0
    t_stop = ticks_ms()
    dt = (t_stop - t_start) / 1000


while True:
    update_P_R()
    refresh_disp(pitch_comp, roll_comp)
