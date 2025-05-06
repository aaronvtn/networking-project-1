# sServer code
from socket import *
import sys
import os

def recvAll(sock, numBytes):
    recvBuff = b''
    while len(recvBuff) < numBytes:
        tmpBuff = sock.recv(numBytes - len(recvBuff))
        if not tmpBuff:
            break
        recvBuff += tmpBuff
    return recvBuff

def recvHeader(sock):
    sizeHeader = recvAll(sock, 10)
    if not sizeHeader:
        return None
    dataSize = int(sizeHeader.decode())
    return recvAll(sock, dataSize)

def sendHeader(sock, dataBytes):
    sizeHeader = str(len(dataBytes)).zfill(10).encode()
    sock.sendall(sizeHeader + dataBytes)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Using: python {sys.argv[0]} <PORT>")

    serverHost = ""
    serverPort = int(sys.argv[1])
    welcomeSock = socket(AF_INET, SOCK_STREAM)
    welcomeSock.bind((serverHost, serverPort))
    welcomeSock.listen(1)
    print("Server is ready.")

    clientSock, addr = welcomeSock.accept()
    print(f"Connection from {addr} to control.")

    while True:
        cmd = clientSock.recv(1024).decode().strip()
        if not cmd:
            break

        parts = cmd.split()
        if parts[0] == "quit":
            print("Client disconnected.")
            break

        elif parts[0] == "ls":
            dataPort = int(parts[1])
            connSock = socket(AF_INET, SOCK_STREAM)
            connSock.connect((addr[0], dataPort))

            file = "\n".join(os.listdir('.')).encode()
            sendHeader(connSock, file)
            connSock.close()
            print("File list printed.")

        elif parts[0] == "get":
            fileName = parts[1]
            dataPort = int(parts[2])
            connSock = socket(AF_INET, SOCK_STREAM)
            connSock.connect((addr[0], dataPort))
            try:
                with open(fileName, 'rb') as my_file:    #rb for raw bytes
                    fileData = my_file.read()
                sendHeader(connSock, fileData)
                print(f"Sent {fileName} which is {len(fileData)} bytes.")
            except FileNotFoundError:
                sendHeader(connSock, b'')
                print("Unable to find file. Please try again.")
            connSock.close()

        elif parts[0] == "put":
            fileName = parts[1]
            dataPort = int(parts[2])
            connSock = socket(AF_INET, SOCK_STREAM)
            connSock.connect((addr[0], dataPort))
            fileData = recvHeader(connSock)
            with open(fileName, 'wb') as my_file:
                my_file.write(fileData)
            print(f"Received {fileName} which is {len(fileData)} bytes")
            connSock.close()

    clientSock.close()
    welcomeSock.close()

