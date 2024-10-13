import socket
import network
from secret import SSID, PASSWD
from time import sleep

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWD)

while not wifi.isconnected():
    print("waiting for connection...")
    sleep(1)

# print(wifi.ifconfig())
server_IP = wifi.ifconfig()[0]
server_port = 2222
buffer_size = 1024

UDPserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPserver.bind((server_IP, server_port))
print(f"Server address is {server_IP}:{server_port}")

while True:
    message, address = UDPserver.recvfrom(buffer_size)
    message_utf = message.decode("utf-8")
    print(message_utf)
    reply = f"message received: {message_utf}".encode("utf-8")
    UDPserver.sendto(reply, address)
