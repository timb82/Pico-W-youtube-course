from machine import Pin, PWM
import utime as time

PIN_BACKWARD = 14
PIN_FORWARD = 15
FREQ = 1000  # Frequency in Hz

pin_f = Pin(PIN_FORWARD, Pin.OUT)
pin_b = Pin(PIN_BACKWARD, Pin.OUT)

# forward
f_pwm = PWM(pin_f)
f_pwm.freq(FREQ)  # Set frequency to 1 kHz
# reverse
r_pwm = PWM(pin_b)
r_pwm.freq(FREQ)  # Set frequency to 1 kHz


try:
    while True:
        for speed in range(20, 101, 10):
            # r_pwm.duty_u16(0)
            # f_pwm.duty_u16(int(speed * 65535 / 100))  # Set duty cycle to speed
            time.sleep(0.25)
            print(speed)

        for speed in range(90, -1, -10):
            # r_pwm.duty_u16(0)
            # f_pwm.duty_u16(int(speed * 65535 / 100))  # Set duty cycle to speed
            time.sleep(0.25)
            print(speed)

        time.sleep(1)


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
