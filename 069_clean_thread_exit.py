import _thread
from devices import Servo
from machine import Pin
from utime import sleep_ms

LED_R_PIN = 15
LED_G_PIN = 14
SERVO_PIN = 16

led_r = Pin(LED_R_PIN, Pin.OUT)
led_g = Pin(LED_G_PIN, Pin.OUT)

del_on = 200
del_off = 200

servo = Servo(SERVO_PIN)
sleep_ms(600)


class Flags:
    flag_blink_r = True
    flag_run = True
    flag_finished = False

    def red_blink(self):
        self.flag_blink_r = True

    def green_blink(self):
        self.flag_blink_r = False

    def run(self):
        self.flag_run = True

    def stop(self):
        self.flag_run = False

    def finished(self):
        self.flag_finished = True

    def not_finished(self):
        self.flag_finished = False


flags = Flags()


def blinker():
    while flags.flag_run:
        if flags.flag_blink_r:
            led_r.on()
            sleep_ms(del_on)
            led_r.off()
            sleep_ms(del_off)
        else:
            led_g.on()
            sleep_ms(del_on)
            led_g.off()
            sleep_ms(del_off)
    led_r.off()
    led_g.off()
    flags.finished()


thr = _thread.start_new_thread(blinker, ())
while flags.flag_run:
    try:
        flags.red_blink()
        for i in range(0, 180, 1):
            servo.angle = i
            sleep_ms(10)

        flags.green_blink()
        for i in range(180, 0, -1):
            servo.angle = i
            sleep_ms(10)
    except KeyboardInterrupt:
        flags.stop()
        servo.angle = 0
        print("waiting for thread to finish... ", end="")
        while not flags.flag_finished:
            print(".", end="")
            sleep_ms(20)
        print("bye")
        break
