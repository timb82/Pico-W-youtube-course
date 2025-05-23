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

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((wlan.ifconfig()[0], 12345))

print("server up and listening")

while True:
    print("waiting for a request...")
    request, client_addr = server_sock.recvfrom(1024)
    print(f"Client request: {request.decode()}")
    print(f"From client: {client_addr}")

    data = str(time.localtime(time.time()))
    server_sock.sendto(data.encode(), client_addr)