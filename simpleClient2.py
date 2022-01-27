# Message Sender
import os
from socket import *
host = "192.168.178.20" # set to IP address of target computer
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
while True:
    data = "test text"
    UDPSock.sendto(data, addr)
 #   if data == "exit":
    break
UDPSock.close()
os._exit(0)