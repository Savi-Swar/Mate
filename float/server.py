import socket
from datetime import datetime
import time

def get_local_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Configure server settings
server_ip = "192.168.13.100" # Listen on all available network interfaces
server_port = 8081

# Create a socket and bind it to the server IP and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))

# Start listening for incoming connections with a maximum queue of 1 connection
server_socket.listen(1)

print(f"Server is listening on {server_ip}:{server_port}")

# Accept incoming connections in a loop
while True:
    client_socket, client_addr = server_socket.accept()
    print(f"Connection from {client_addr}")

    data = client_socket.recv(1024).decode("utf-8")
    print(f"Received data: {data}")

    if data == "check_start_signal":

        local_time = get_local_time() + '\n'
        print(local_time)
        start_signal = input("Enter 'start' to start the program or anything else to wait: ")
        start_signal += '\n'
        # client_socket.sendall(local_time.encode('utf-8'))
        # client_socket.sendall(start_signal.encode("utf-8"))
        
        # Send the local time with a delimiter (e.g., '|')
        

        print("Raw data:", data.encode("utf-8"))  # This will print the raw bytes received

    else:
        # Process the received data as before
        print(f"Received data: {data}")

    client_socket.close()

# Close the server socket (this line will not be reached in the current implementation)
server_socket.close()
