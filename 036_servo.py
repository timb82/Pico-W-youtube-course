import uasyncio as asyncio
from machine import Pin, PWM, I2C
from ssd1306 import SSD1306_I2C
from rotary_encoder import RotaryEncoderRP2, RotaryEncoderEvent

# Constants
ENCODER_CLK_PIN = 28
ENCODER_DT_PIN = 27
ENCODER_SW_PIN = 26
OLED_SDA_PIN = 6
OLED_SCL_PIN = 7
OLED_I2C_CHN = 1
SERVO_PIN = 16


def duty(deg):
    a = (2.5e6 - 0.5e6) / 180
    b = 0.5e6
    return int(a * deg + b)


# Devices
i2c = I2C(id=OLED_I2C_CHN, sda=OLED_SDA_PIN, scl=OLED_SCL_PIN)
dsp = SSD1306_I2C(128, 64, i2c)
servo = PWM(Pin(SERVO_PIN))
servo.freq(50)

# Define the pins for the rotary encoder and the button
enc_pin_clk = Pin(ENCODER_CLK_PIN, Pin.IN, Pin.PULL_UP)
enc_pin_dt = Pin(ENCODER_DT_PIN, Pin.IN, Pin.PULL_UP)
enc_pin_sw = Pin(ENCODER_SW_PIN, Pin.IN, Pin.PULL_UP)
enc = RotaryEncoderRP2(
    pin_clk=enc_pin_clk,
    pin_dt=enc_pin_dt,
    pin_sw=enc_pin_sw,
    half_step=True,
    fast_ms=0,
)
angle = 0


def angle_update():
    global angle
    dsp.fill(0)
    dsp.text(str(angle), 20, 20)
    dsp.show()
    print(angle)
    servo.duty_ns(duty(angle))


# Events
def turn_left_listener():
    global angle
    if angle >= 1:
        angle -= 1
    angle_update()


def turn_left_fast_listener():
    global angle
    if angle >= 10:
        angle -= 10
    else:
        angle = 0
    angle_update()


def turn_right_listener():
    global angle
    if angle < 180:
        angle += 1
    angle_update()


def turn_right_fast_listener():
    global angle
    if angle < 170:
        angle += 10
    else:
        angle = 180
    angle_update()


def multi_click_listener(clicks):
    global angle
    angle = 90
    angle_update()


# Subscriptions
# enc.on(RotaryEncoderEvent.ANY, any_event_listener)
# enc.on(RotaryEncoderEvent.CLICK, single_click_listener)
enc.on(RotaryEncoderEvent.MULTIPLE_CLICK, multi_click_listener)
# enc.on(RotaryEncoderEvent.HELD, held_listener)
# enc.on(RotaryEncoderEvent.RELEASED, released_listener)
enc.on(RotaryEncoderEvent.TURN_LEFT, turn_left_fast_listener)
enc.on(RotaryEncoderEvent.TURN_LEFT_HOLD, turn_left_listener)
# enc.on(RotaryEncoderEvent.TURN_LEFT_FAST, turn_left_fast_listener)
# enc.on(RotaryEncoderEvent.TURN_LEFT_FAST_HOLD, turn_left_fast_hold)
enc.on(RotaryEncoderEvent.TURN_RIGHT, turn_right_fast_listener)
enc.on(RotaryEncoderEvent.TURN_RIGHT_HOLD, turn_right_listener)
# enc.on(RotaryEncoderEvent.TURN_RIGHT_FAST, turn_right_fast_listener)
# enc.on(RotaryEncoderEvent.TURN_RIGHT_FAST_HOLD, turn_right_fast_hold)


# while True:
#     pass
# angle = int(input("What angle should I set? "))
# servo.duty_ns(duty(angle))
asyncio.run(enc.async_tick())
