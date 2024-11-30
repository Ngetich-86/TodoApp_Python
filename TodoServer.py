import socket
import ssl
import threading # Multithreading support

# In-memory storage for tasks per user
tasks = {}

# Authentication data (for simplicity)
users = {"Ngetich": "password", "user2": "password2"}

def handle_client(connection, address):
    print(f"[INFO] Client connected: {address}")
    connfile = connection.makefile("rw")

    try:
        connfile.write("Welcome to the To-Do List Manager!\n")
        connfile.write("Please log in (format: username password):\n")
        connfile.flush() # Flush the buffer to send the message

        credentials = connfile.readline().strip().split()
        if len(credentials) != 2 or credentials[0] not in users or users[credentials[0]] != credentials[1]:
            connfile.write("Invalid credentials. Disconnecting.\n")
            connfile.flush()
            return

        username = credentials[0]
        if username not in tasks:
            tasks[username] = []

        connfile.write(f"Welcome, {username}!\n")
        connfile.write("Commands: add <task>, view, complete <task_no>, exit\n")
        connfile.flush()

        while True:
            connfile.write("Enter a command: ")
            connfile.flush()
            command = connfile.readline().strip()

            if not command:
                break

            if command.startswith("add "):
                task = command[4:]
                tasks[username].append(task)
                connfile.write(f"Task added: {task}\n")

            elif command == "view":
                connfile.write("Your tasks:\n")
                for idx, task in enumerate(tasks[username], 1):
                    connfile.write(f"{idx}. {task}\n")

            elif command.startswith("complete "):
                try:
                    task_no = int(command.split()[1]) - 1
                    if 0 <= task_no < len(tasks[username]):
                        completed_task = tasks[username].pop(task_no)
                        connfile.write(f"Task completed: {completed_task}\n")
                    else:
                        connfile.write("Invalid task number.\n")
                except (IndexError, ValueError):
                    connfile.write("Invalid command format. Use: complete <task_no>\n")

            elif command == "exit":
                connfile.write("Goodbye!\n")
                break

            else:
                connfile.write("Unknown command.\n")

            connfile.flush()

    except Exception as e:
        print(f"[ERROR] Exception handling client {address}: {e}")

    finally:
        connection.close()
        print(f"[INFO] Client disconnected: {address}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))
    server_socket.listen(5)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    print("[INFO] Server started. Awaiting connections...") # Print a message to indicate that the server is running
    while True:
        client_socket, addr = server_socket.accept()
        secure_socket = context.wrap_socket(client_socket, server_side=True)

        threading.Thread(target=handle_client, args=(secure_socket, addr)).start()

if __name__ == "__main__":
    start_server()
