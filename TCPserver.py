from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print(f"[+] Server is Listening for incoming Client Requests!!!")
while True:
    connectionSocket, addr = serverSocket.accept()
    messagefromclient = str(connectionSocket.recv(1024),'utf-8')
    print(f"[+] Message from Client: {messagefromclient}")
    messagefromserver = input("Enter reply message for client: ")
    connectionSocket.send (bytes(messagefromserver, 'utf-8'))