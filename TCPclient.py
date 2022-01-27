from socket import *
serverName = '192.168.178.20'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
while True:
	messagetoserver = input("Enter Message for Server: ")
	clientSocket.send(bytes(messagetoserver, 'utf-8'))
	replyfromserver = str(clientSocket.recv(1024),'utf-8')
	print(f"[+] Reply Message from Server: {replyfromserver}")

clientSocket.close()