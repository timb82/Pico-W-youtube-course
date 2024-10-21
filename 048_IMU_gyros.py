from machine import I2C
from time import sleep_ms, ticks_ms
from imu import MPU6050
# from ssd1306 import SSD1306_I2C

OLED_SDA_PIN = 6
OLED_SCL_PIN = 7
OLED_I2C_CHN = 1


# i2c_imu = I2C(IMU_I2C_CHN, sda=Pin(IMU_SDA_PIN), scl=Pin(IMU_SCL_PIN), freq=400000)
i2c = I2C(id=OLED_I2C_CHN, sda=OLED_SDA_PIN, scl=OLED_SCL_PIN)

mpu = MPU6050(i2c)

pitch = 0
roll = 0
yaw = 0
dt = 0
cntr = 0
# zs=[]
while True:
    t_start = ticks_ms()
    gx = mpu.gyro.x - 0.05022978
    gy = mpu.gyro.y - 1.5504778
    gz = mpu.gyro.z - 0.799  # 0.8015522
    roll = roll + gy * dt
    pitch = pitch + gx * dt
    yaw = yaw + gz * dt
    #     zs.append(gy)
    sleep_ms(10)
    cntr += 1
    if cntr == 50:
        #        print(f"x={gx:+0.6f}, y={gy:+0.6f}, z={gz:+0.6f}")
        #        zs = [sum(zs)/len(zs)]
        #        print(f"yaw={yaw}\t z_s={zs[0]}\t{dt}")
        #        print(zs[0])
        print(f"pitch={pitch}, roll={roll}, yaw={yaw}")
        cntr = 0
    t_stop = ticks_ms()
    dt = (t_stop - t_start) / 1000
