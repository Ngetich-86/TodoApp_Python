import socket
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get host and port from environment variables
host = os.getenv('HOST', '127.0.0.1')  # Default to localhost
port = int(os.getenv('PORT', 12345))   # Default to port 12345

# In-memory storage for tasks per user
tasks = {}

# Authentication data (for simplicity)
users = {"Ngetich": "password1", "user2": "password2"}


def handle_client(client_socket):
    try:
        # Authentication process
        while True:
            client_socket.send("Please log in (format: username password): ".encode('utf-8'))
            credentials = client_socket.recv(1024).decode('utf-8').strip().split()

            if len(credentials) != 2 or credentials[0] not in users or users[credentials[0]] != credentials[1]:
                client_socket.send("Invalid credentials. Disconnecting.\n".encode('utf-8'))
                break

            username = credentials[0]
            if username not in tasks:
                tasks[username] = []
            client_socket.send(f"Welcome, {username}!\n".encode('utf-8'))
            break

        # Main to-do commands
        while True:
            client_socket.send("Commands: add <task>, view, complete <task_no>, exit\n".encode('utf-8'))
            command = client_socket.recv(1024).decode('utf-8').strip()

            if command.startswith("add "):
                task = command[4:]
                tasks[username].append(task)
                client_socket.send(f"Task added: {task}\n".encode('utf-8'))

            elif command == "view":
                client_socket.send("Your tasks:\n".encode('utf-8'))
                for idx, task in enumerate(tasks[username], 1):
                    client_socket.send(f"{idx}. {task}\n".encode('utf-8'))

            elif command.startswith("complete "):
                try:
                    task_no = int(command.split()[1]) - 1
                    if 0 <= task_no < len(tasks[username]):
                        completed_task = tasks[username].pop(task_no)
                        client_socket.send(f"Task completed: {completed_task}\n".encode('utf-8'))
                    else:
                        client_socket.send("Invalid task number.\n".encode('utf-8'))
                except (IndexError, ValueError):
                    client_socket.send("Invalid command format. Use: complete <task_no>\n".encode('utf-8'))

            elif command == "exit":
                client_socket.send("Goodbye!\n".encode('utf-8'))
                break

            else:
                client_socket.send("Unknown command.\n".encode('utf-8'))

    except Exception as e:
        print(f"[ERROR] Exception handling client: {e}")
    finally:
        client_socket.close()


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"[INFO] Server started on {host}:{port}. Awaiting connections...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"[INFO] Client connected: {addr}")
            handle_client(client_socket)


if __name__ == "__main__":
    start_server()
