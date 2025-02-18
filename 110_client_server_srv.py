import network
import usocket as socket
import utime as time
from machine import Pin
from secrets import SSID, PASSWD

led_r = Pin(18, Pin.OUT)
led_g = Pin(20, Pin.OUT)
led_y = Pin(19, Pin.OUT)


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

def set_color(color):
    if color == 'red':
        led_r.on()
        led_g.off()
        led_y.off()
    elif color == 'green':
        led_r.off()
        led_g.on()
        led_y.off()
    elif color == 'yellow':
        led_r.off()
        led_g.off()
        led_y.on()
    else:
        led_r.off()
        led_g.off()
        led_y.off()


while True:
    print("waiting for a request...")
    request, client_addr = server_sock.recvfrom(1024)
    print(f"Client request: {request.decode()}")
    print(f"From client: {client_addr}")

    data = request.decode()
    set_color(data)
    server_sock.sendto(data.encode(), client_addr)






