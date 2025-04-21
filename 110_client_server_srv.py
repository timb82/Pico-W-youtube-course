import network
import usocket as socket
import utime as time
from machine import Pin, Timer
from secrets import SSID, PASSWD

led_r = Pin(18, Pin.OUT)
led_g = Pin(20, Pin.OUT)
led_y = Pin(19, Pin.OUT)

freq = 2
active_led = None
t = None

print("connecting WiFi...")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWD)

while not wlan.isconnected():
    time.sleep(0.01)

print("WiFi connected")
print(wlan.ifconfig())

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((wlan.ifconfig()[0], 12345))

print("server up and listening")


def blinker(Source):
    if active_led is not None:
        active_led.toggle()


def ticker():
    t = Timer(period=int(1 / (freq * 2) * 1000), mode=Timer.PERIODIC, callback=blinker)
    return t


def set_color(color):
    global active_led
    global t
    if t is not None:
        t.deinit()
        del t

    if color == "red":
        led_r.on()
        led_g.off()
        led_y.off()
        active_led = led_r
    elif color == "green":
        led_r.off()
        led_g.on()
        led_y.off()
        active_led = led_g
    elif color == "yellow":
        led_r.off()
        led_g.off()
        led_y.on()
        active_led = led_y

    elif color[0:4] == "freq":
        global freq
        freq = float(color.split("=")[-1])
        if t is not None:
            t.deinit()
        if freq > 0 and active_led is not None:
            t = ticker()

    else:
        active_led = None
        led_r.off()
        led_g.off()
        led_y.off()
        t = None

    if freq > 0 and active_led is not None:
        active_led = led_r
        t = ticker()


while True:
    print("waiting for a request...")
    request, client_addr = server_sock.recvfrom(1024)
    print(f"Client request: {request.decode()}")
    print(f"From client: {client_addr}")

    data = request.decode()
    set_color(data)
    server_sock.sendto(data.encode(), client_addr)
