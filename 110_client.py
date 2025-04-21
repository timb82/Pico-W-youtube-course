import socket
import time

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
srv_addr = ("192.168.1.92", 12345)

while True:
    request_msg = input("pick color (red, green, yellow, off): ")
    client_sock.sendto(request_msg.encode(), srv_addr)
    data, addr = client_sock.recvfrom(1024)
    print(f"received data: {data.decode()}")
