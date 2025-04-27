import network
import usocket as socket
import utime as time
from machine import PWM, Pin
from secrets import SSID, PASSWD

freq = 1000
led_g = PWM(Pin(19))
led_r = PWM(Pin(18))
led_b = PWM(Pin(20))

led_g.freq(freq)
led_r.freq(freq)
led_b.freq(freq)
# WiFi connection setup
print("connecting WiFi...")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWD)

# Wait for connection
while not wlan.isconnected():
    time.sleep(0.01)
print("WiFi connected")
print(wlan.ifconfig())

# Setup UDP server
server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((wlan.ifconfig()[0], 54321))
print("server up and listening")
print(wlan.ifconfig()[0])


while True:
    # print("waiting for a request...")
    request, client_addr = server_sock.recvfrom(1024)
    my_color = request.decode()
    my_color = my_color.split(",")
    my_color = [int(c) for c in my_color]
    # print(f"Client request: {my_color}")
    # print(f"From client: {client_addr}")

    led_r.duty_u16(int(my_color[0] / 255 * 65535))
    led_g.duty_u16(int(my_color[1] / 255 * 65535))
    led_b.duty_u16(int(my_color[2] / 255 * 65535))

    response = f"LED {str(my_color)} executed"
    server_sock.sendto(str(my_color).encode(), client_addr)
    # print("data sent")
