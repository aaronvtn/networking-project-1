# Server code
from socket import *
import sys

if __name__ == "__main__":

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


    # Define a function to receive all bytes from client
    def recv_all(socket, num_bytes):
        # The buffer
        recv_buff = ""
        
        # The temporary buffer
        tmp_buff = ""
        
        # Keep receiving until all is received
        while len(recv_buff) < num_bytes:
            
            # Attempt to receive bytes
            tmp_buff = socket.recv(num_bytes)
            
            # The other side has closed the socket
            if not tmp_buff:
                break
            
            # Add the received bytes to the buffer
            if type(tmp_buff) == bytes:
                tmp_buff = tmp_buff.decode('utf-8')

            recv_buff += tmp_buff
        
        return recv_buff


    # Continually accept incoming connections
    while(True):
        # Accept a connection and get client's socket
        connection_socket, addr = server_socket.accept()
        print(f"Connected by {addr}\n")

        # Buffer for all data received from client
        file_data = ""
        # Size of the incoming file as marked in the size header
        file_size = 0
        # Buffer containing the file size
        file_size_buff = ""

        # Receive the first 10 bytes indicating the size of the file
        file_size_buff = recv_all(connection_socket, 10)
            
        # Get the file size
        file_size = int(file_size_buff)
        
        
        print(f'The file size is {file_size}')
        # Get the file data
        file_data = recv_all(connection_socket, file_size)
        print(f'The file data is:\n{file_data}')
            
        # Close our side
        connection_socket.close()
        sys.exit()