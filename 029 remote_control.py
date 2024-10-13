import socket
from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
from network import WLAN, STA_IF
from secret import SSID, PASSWD
from time import sleep

RPIN = 13
GPIN = 11
BPIN = 10


# Setup hardware
i2c = I2C(id=1, sda=Pin(6), scl=Pin(7))
disp = SSD1306_I2C(128, 64, i2c)
wifi = WLAN(STA_IF)

led = [PWM(Pin(RPIN)), PWM(Pin(GPIN)), PWM(Pin(BPIN))]
rgb = [0, 0, 0]


def update_led(rgb):
    for l, val in zip(led, rgb):
        l.freq(1000)
        l.duty_u16(int(val / 100 * (2**16 - 1)))


wifi.active(True)
wifi.connect(SSID, PASSWD)

print("connecting")
while not wifi.isconnected():
    disp.text("connecting...", 0, 0)
    disp.show()
    sleep(1)
server_IP = wifi.ifconfig()[0]
print("connected as ", server_IP)
server_port = 2222
buff_size = 1024
UDPserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPserver.bind((server_IP, server_port))
disp.fill(0)
disp.text(f"IP: {server_IP}", 0, 0)
disp.show()

while True:
    message, address = UDPserver.recvfrom(buff_size)
    message_utf = message.decode("utf-8")
    try:
        vals = [int(i) for i in message_utf.split(",")]
        if len(vals) != 3:
            raise ValueError
        disp.rect(0, 10, 128, 50, 0, True)
        disp.text(f"{vals[0]}, {vals[1]}, {vals[2]}", 24, 0, 1)
        disp.show()
        update_led(vals)

    except ValueError:
        print("wrong value")
        disp.rect(0, 10, 128, 50, 0, True)
        disp.text("wrong value", 24, 0, 1)
        disp.show()
    print(message_utf)
    reply = f"message received: {message_utf}".encode("utf-8")
    UDPserver.sendto(reply, address)
