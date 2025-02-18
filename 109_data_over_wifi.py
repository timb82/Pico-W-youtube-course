import network
import usocket as socket
import utime as time
from secrets import SSID, PASSWD

print("connecting WiFi...")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWD)

while not wlan.isconnected():
    time.sleep(0.01)

print("WiFi connected")
print(wlan.ifconfig())

s_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_sock.bind(wlan.ifconfig()[0], 12345)
