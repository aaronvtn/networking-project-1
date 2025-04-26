# Client code
from socket import *
import sys


if __name__ == "__main__":

    # Command line checks 
    if len(sys.argv) < 2:
        sys.exit(f'USAGE: python {sys.argv[0]} <FILENAME>')

    # Name and port number of the server to connect to
    server_name = "127.0.0.1"
    server_port = 12000

    # Store the file name provided by the user
    file_name = sys.argv[1]

    # Open the file in read mode
    file_obj = open(file_name, "r")

    # Create a socket
    client_socket = socket(AF_INET, SOCK_STREAM)

    # Connect to the server
    client_socket.connect((server_name, server_port))

    # # String we want to send to the server - NOTE: Commenting this out for the file sending version
    # data = "Hello world! This is a very long string"

    # Keep track of bytes sent and the file data
    bytes_sent = 0
    file_data = None

    # Read in the file data
    while True:
        file_data = file_obj.read(65536)

        if file_data:
            # Get the size of the data read and convert it to string
            size_header = str(len(file_data))
            
            # Prepend 0's to the size header until the size is 10 bytes
            while len(size_header) < 10:
                size_header = "0" + size_header
        
            # Prepend the size header to the file data.
            file_data = size_header + file_data	
            
            # Send the data!
            while bytes_sent != len(file_data):
                bytes_sent += client_socket.send(file_data[bytes_sent:].encode())

        else:
            break

    print(f'Sent {bytes_sent} bytes.')
    
    # Close the socket and the file
    client_socket.close()
    file_obj.close()