from machine import Pin
import utime as time

PIN_BACKWARD = 14
PIN_FORWARD = 15

pin_f = Pin(PIN_FORWARD, Pin.OUT)
pin_b = Pin(PIN_BACKWARD, Pin.OUT)

previous_state = "0"
direction = "0"


# forward
def forward():
    pin_b.off()
    pin_f.on()


# backward
def backward():
    pin_f.off()
    pin_b.on()


# stop
def stop():
    pin_f.off()
    pin_b.off()


stop()
time.sleep(1)
try:
    while True:
        direction = input("Enter direction (F/B/0): ").strip().lower()

        if direction == "f":
            if previous_state == "b":
                stop()
                time.sleep(1)
            forward()
        elif direction == "b":
            if previous_state == "f":
                stop()
                time.sleep(1)
            backward()
        elif direction == "0":
            stop()
        else:
            print("Invalid input. Please enter 'F', 'B', or '0'.")
        print(f"motor status: {direction}")
        previous_state = direction
except KeyboardInterrupt:
    stop()
    direction = "0"
    previous_state = "0"
    print(f"motor status: {direction}")
except Exception as e:
    print(f"An error occurred: {e}")
