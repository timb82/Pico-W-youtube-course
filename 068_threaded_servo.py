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

flag_blink = True
flag_run = True
flag_finished = False


def blinker():
    global flag_finished
    while flag_run:
        if flag_blink:
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
    flag_finished = True
    return None


thr = _thread.start_new_thread(blinker, ())
while flag_run:
    try:
        flag_blink = True
        for i in range(0, 180, 1):
            servo.angle = i
            sleep_ms(10)

        flag_blink = False
        for i in range(180, 0, -1):
            servo.angle = i
            sleep_ms(10)
    except KeyboardInterrupt:
        flag_run = False
        print("waiting for thread to finish... ", end="")
        while not flag_finished:
            print(".", end="")
            sleep_ms(20)
        break
