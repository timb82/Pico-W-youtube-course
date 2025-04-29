from machine import Pin, PWM
import utime as time

PIN_BACKWARD = 14
PIN_FORWARD = 15
FREQ = 1000  # Frequency in Hz


class MotorDC:
    def __init__(self, freq):
    self.pin_f = Pin(PIN_FORWARD, Pin.OUT)
    self.pin_b = Pin(PIN_BACKWARD, Pin.OUT)

    # forward
    self.f_pwm = PWM(self.pin_f)
    self.f_pwm.freq(freq)  # Set frequency to 1 kHz
    # reverse
    self.r_pwm = PWM(self.pin_b)
    self.r_pwm.freq(freq)  # Set frequency to 1 kHz


try:
    while True:
        r_pwm.duty_u16(0)
        f_pwm.duty_u16(0)

        for speed in range(20, 101, 10):
            # f_pwm.duty_u16(int(speed * 65535 / 100))  # Set duty cycle to speed
            time.sleep(0.25)
            print(speed)

        for speed in range(90, -1, -10):
            # f_pwm.duty_u16(int(speed * 65535 / 100))  # Set duty cycle to speed
            time.sleep(0.25)
            print(speed)

        r_pwm.duty_u16(0)
        f_pwm.duty_u16(0)
        time.sleep(2)

        for speed in range(20, 101, 10):
            # r_pwm.duty_u16(int(speed * 65535 / 100))  # Set duty cycle to speed
            time.sleep(0.25)
            print(speed)

        for speed in range(90, -1, -10):
            # r_pwm.duty_u16(int(speed * 65535 / 100))  # Set duty cycle to speed
            time.sleep(0.25)
            print(speed)



except KeyboardInterrupt:
    r_pwm.duty_u16(0)
    f_pwm.duty_u16(0)
    f_pwm.deinit()
    r_pwm.deinit()
    pin_f.off()
    pin_b.off()
    print("Program stopped.")
except Exception as e:
    print(f"An error occurred: {e}")
