from machine import Pin, PWM
from utime import sleep_ms


class Servo:
    def __init__(self, pin_no, freq=50, angle=0):
        self._out = PWM(Pin(pin_no, Pin.OUT))
        self._angle = angle
        self._out.duty_ns(self._ang2duty(self._angle))
        self._out.freq(freq)

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
        return self._out.duty_ns()

    @duty.setter
    def duty(self, duty):
        # self._duty = duty
        self._out.duty_ns(duty)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle
        self.duty = self._ang2duty(self._angle)


if __name__ == "__main__":
    from devices import Joystick, LED

    JOY_X_PIN = 27
    JOY_Y_PIN = 26
    JOY_SW_PIN = 17
    SERVO_PIN = 16
    LED_PIN = 15

    joy = Joystick(JOY_X_PIN, JOY_Y_PIN, JOY_SW_PIN)
    servo = Servo(SERVO_PIN, angle=90)
    sw_last = 0
    led = LED(15)

    incremental_control = True  # switch beween incremental control based on x-axis and 1 for direct angle control
    led._pin.value(int(incremental_control))

    while True:
        angle = servo.angle
        if incremental_control:
            # Incremental control on X-axis of the joystick
            if joy.pos[0] < -12 and angle <= 180:
                angle = angle - joy.pos[0] / 20
            elif joy.pos[0] > 12 and angle >= 0:
                angle = angle - joy.pos[0] / 20
        else:
            # Direct angle control
            angle = joy.angle
            if angle > 180:
                angle = 360 - angle

        # print(f"{incremental_control}\t{joy.sw}\t{angle}")

        # Switch changes control mode between incremental and direct angle
        sw = joy.sw
        if sw_last == 0 and sw == 1:
            incremental_control = bool(incremental_control ^ True)
            led._pin.value(int(incremental_control))
        sw_last = sw

        if angle > 180:
            angle = 180
        elif angle < 0:
            angle = 0
        servo.angle = angle
        sleep_ms(50)
