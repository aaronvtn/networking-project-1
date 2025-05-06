# client.py
from socket import *
import sys
import os
#could not use commands import due to using python 3.13

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

def createSocket():
    connSock = socket(AF_INET, SOCK_STREAM)
    connSock.bind(('', 0))
    connSock.listen(1)
    return connSock, connSock.getsockname()[1]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(f"Using: python {sys.argv[0]} <SERVER_HOST> <SERVER_PORT>")

    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])

    clientSock = socket(AF_INET, SOCK_STREAM)
    clientSock.connect((serverName, serverPort))
    print("Connection Succesful.")

    while True:
        cmd = input("ftp> ").strip()
        if not cmd:
            continue
        parts = cmd.split()

        if parts[0] == "quit":
            clientSock.sendall(cmd.encode())
            break

        elif parts[0] == "ls":
            connSock, dataPort = createSocket()
            clientSock.sendall(f"ls {dataPort}".encode())
            conn, _ = connSock.accept()
            data = recvHeader(conn)
            print(data.decode())
            conn.close()
            connSock.close()

        elif parts[0] == "get" and len(parts) == 2:
            fileName = parts[1]
            connSock, dataPort = createSocket()
            clientSock.sendall(f"get {fileName} {dataPort}".encode())
            conn, _ = connSock.accept()
            fileData = recvHeader(conn)
            if fileData:
                with open(fileName, 'wb') as my_file:
                    my_file.write(fileData)
                print(f"Received {fileName} which is {len(fileData)} bytes.")
            else:
                print("Unable to find file on server. Please try again.")
            conn.close()
            connSock.close()

        elif parts[0] == "put" and len(parts) == 2:
            fileName = parts[1]
            if not os.path.exists(fileName):
                print("Unable to find file. Please try again.")
                continue
            connSock, dataPort = createSocket()
            clientSock.sendall(f"put {fileName} {dataPort}".encode())
            conn, _ = connSock.accept()
            with open(fileName, 'rb') as f:
                fileData = f.read()
                sendHeader(conn, fileData)
            print(f"Sent {fileName} which is {len(fileData)} bytes.")
            conn.close()
            connSock.close()

        else:
            print("Incorrect command, please try again.")

    clientSock.close()
