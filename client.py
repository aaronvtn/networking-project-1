# Client code
from socket import *

# Name and port number of the server to connect to
server_name = "ecs.fullerton.edu"
server_port = 12000

# Create a socket
client_socket = socket(AF_INET, SOCK_STREAM)

# Connect to the server
client_socket.connect((server_name, server_port))

# String we want to send to the server
data = "Hello world! This is a very long string"

bytes_sent = 0

# Keep sending bytes until all bytes are sent
while bytes_sent != len(data):
    bytes_send += client_socket.send(data[bytes_sent:])

client_socket.close()