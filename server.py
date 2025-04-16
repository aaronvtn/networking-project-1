# Server code
from socket import *

# Localhost
server_host = "127.0.0.1"

# Listen port
server_port = 12000

# Creating a TCP socket
server_socket = socket(AF_INET, SOCK_STREAM)

# Binding socket to local host and port
server_socket.bind((server_host, server_port))

# Start listening for incoming connections
server_socket.listen(1)
print("The server is ready to receive!")

# Buffer to store received data
data = ""

# Continually accept incoming connections
while(True):
    # Accept a connection and get client's socket
    connection_socket, addr = server_socket.accept()
    print(f"Connected by {addr}")

    # Temporary buffer
    tmp_buff = ""

    while len(data) != 40:
        # Receive whatever the newly connected client has to send
        tmp_buff = connection_socket.recv(40)
        if not tmp_buff:
            break
        data += tmp_buff

    print(data)

connection_socket.close() # Unsure if this goes inside or outside the while loop