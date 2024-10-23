from machine import Pin
from time import sleep

LED_R_PIN = 15
LED_G_PIN = 14


class LED:
    def __init__(self, led_pin):
        self._pin = Pin(led_pin, Pin.OUT)

    def _close(self):
        self._pin.off()

    def blink(self, blinks_no, delay):
        for i in range(0, blinks_no):
            self._pin.on()
            sleep(delay)
            self._pin.off()
            sleep(delay)

    def on(self):
        self._pin.on()

    def off(self):
        self._pin.off()


if __name__ == "__main__":
    LED_R_PIN = 15
    LED_G_PIN = 14
    led_r = LED(LED_R_PIN)
    led_g = LED(LED_G_PIN)

    while True:
        try:
            led_r.blink(5, 0.5)
            led_g.blink(10, 0.1)
        except KeyboardInterrupt:
            led_r._close()
            led_g._close()
            break
