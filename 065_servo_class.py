from machine import Pin, PWM
from utime import sleep_ms


class Servo:
    def __init__(self, pin_no, freq=50, duty=0, angle=0):
        self._out = PWM(Pin(pin_no))
        self._duty = 0
        self._freq = freq
        self._angle = 0

    def _ang2duty(self, angle):
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180
        return int(angle * 1e5 / 9 + 5e5)

    def _duty2ang(self, duty):
        if duty < 500_000:
            duty = 500_000
        elif duty > 2_500_000:
            duty = 2_500_000
        return round(duty * 180 / 2e6 - 45, 2)

    @property
    def duty(self):
        return self._duty

    @duty.setter
    def duty(self, duty):
        self._duty = duty
        self._angle = self._duty2ang(duty)
        self._out.duty_ns(self._duty)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle
        print("cha ching")
        self.duty = self._ang2duty(self._angle)


if __name__ == "__main__":
    from devices import Joystick

    JOY_X_PIN = 27
    JOY_Y_PIN = 26
    JOY_SW_PIN = 17
    SERVO_PIN = 16

    joy = Joystick(JOY_X_PIN, JOY_Y_PIN, JOY_SW_PIN)
    servo = Servo(SERVO_PIN, angle=90)

    while True:
        angle = servo.angle
        print(f"{joy.pos[0]}\t {angle}\t {servo.duty}")
        if joy.pos[0] < -12 and angle <= 180:
            print("ping")
            angle = angle - joy.pos[0] / 10
        elif joy.pos[0] > 12 and angle >= 0:
            print("pong")
            angle = angle - joy.pos[0] / 10

        if angle > 180:
            angle = 180
        elif angle < 0:
            angle = 0
        servo.angle = angle
        sleep_ms(150)
