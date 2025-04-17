# Client code
from socket import *


if __name__ == "__main__":

    # Name and port number of the server to connect to
    server_name = "127.0.0.1"
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
        bytes_sent += client_socket.send(data[bytes_sent:].encode())

    client_socket.close()