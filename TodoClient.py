import socket
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get host and port from environment variables
host = os.getenv('HOST', '127.0.0.1')  # Default to localhost
port = int(os.getenv('PORT', 12345))   # Default to port 12345


def handle_authenticate(client_socket):
    while True:
        response = client_socket.recv(1024).decode('utf-8').strip()
        print("Received:", response)
        
        if "Please log in (format: username password):" in response:
            credentials = input(response).strip()
            client_socket.send(credentials.encode('utf-8'))
        
        elif "Welcome" in response:
            print(response)
            return True
        
        elif "Invalid credentials" in response:
            print(response)
            break


def add_task(client_socket):
    while True:
        response = client_socket.recv(1024).decode('utf-8').strip()
        if "Commands: add <task>, view, complete <task_no>, exit" in response:
            print(response)
            task = input("Enter a new task: ")
            client_socket.send(f"add {task}".encode('utf-8'))
            continue
        print(response)


def view_tasks(client_socket):
    while True:
        response = client_socket.recv(1024).decode('utf-8').strip()
        if "Your tasks:" in response:
            print(response)
            continue
        print(response)


def complete_task(client_socket):
    while True:
        response = client_socket.recv(1024).decode('utf-8').strip()
        if "Enter task number to complete:" in response:
            print(response)
            task_no = input("Task number: ")
            client_socket.send(f"complete {task_no}".encode('utf-8'))
            continue
        print(response)


def handle_client(client_socket):
    try:
        if handle_authenticate(client_socket):
            while True:
                response = client_socket.recv(1024).decode('utf-8').strip()
                print(response)
                
                if "Commands: add <task>, view, complete <task_no>, exit" in response:
                    action = input("Choose an action: ")
                    if action == "add":
                        add_task(client_socket)
                    elif action == "view":
                        view_tasks(client_socket)
                    elif action == "complete":
                        complete_task(client_socket)
                    elif action == "exit":
                        print("Goodbye!")
                        client_socket.send("exit".encode('utf-8'))
                        break
                    else:
                        print("Invalid command. Try again.")
                else:
                    print("Unexpected response, disconnecting.")
                    break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            handle_client(client_socket)
        except Exception as e:
            print(f"An error occurred: {e}")
            client_socket.close()