from machine import Pin
from utime import sleep
import _thread as thread
from sys import exit


LED_R_PIN = 15
LED_G_PIN = 14

led_r = Pin(LED_R_PIN, Pin.OUT)
led_g = Pin(LED_G_PIN, Pin.OUT)

red_on = 1.5
red_off = 1.5
red_blinks = 2
green_on = 0.3
green_off = 0.3
green_blinks = 10
run_flag = True


def red_blink():
    while run_flag:
        led_r.on()
        sleep(red_on)
        led_r.off()
        sleep(red_off)


def green_blink():
    while run_flag:
        led_g.on()
        sleep(green_on)
        led_g.off()
        sleep(green_off)


try:
    thread.start_new_thread(red_blink, ())
    green_blink()
except KeyboardInterrupt:
    run_flag = False
    led_r.off()
    led_g.off()
    print("bye")
    exit()
