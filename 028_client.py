import socket

server_addr = ("192.168.1.92", 2222)
buff_size = 1024
UDPclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = input("What is your command? ").encode("utf-8")
    UDPclient.sendto(message, server_addr)
    data, addr = UDPclient.recvfrom(buff_size)
    print(data.decode("utf-8"))
