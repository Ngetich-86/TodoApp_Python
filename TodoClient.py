import socket # Socket programming
import ssl # Secure Sockets Layer

def start_client():# Function to start the client
    context = ssl.create_default_context() # Create a default SSL context
    context.check_hostname = False # Disable hostname verification
    context.verify_mode = ssl.CERT_NONE # Disable certificate verification

    with socket.create_connection(("localhost", 12345)) as sock: # Create a connection to the server
        with context.wrap_socket(sock, server_hostname="localhost") as secure_socket: # Wrap the socket with SSL
            print("[INFO] Connected to the server.")
            connfile = secure_socket.makefile("rwb", buffering=0) # Create a file-like object for the connection

            while True:
                response = connfile.readline().decode() # Read a line from the connection
                if not response:
                    break
                print(response.strip()) 

                if "Enter a command:" in response:
                    command = input("> ") + "\n"
                    connfile.write(command.encode())

if __name__ == "__main__": # If the script is run directly
    start_client()
