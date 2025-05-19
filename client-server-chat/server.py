import socket
import threading


HOST = "127.0.01"

# Port numbers range from 0 to 65535. Ports 0-1023 are reserved for system services, so we use a port above 1023.
PORT = 12346 

HEADER = 1024
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        # Receive the message length from the client
        msg_length = int(conn.recv(HEADER).decode(FORMAT))
        if msg_length:
            # Receive the message from the client
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}")

    print(f"[DISCONNECTED] {addr} disconnected.")
    conn.close()

def start():
    server.listen()
    conn, addr = server.accept()
    print(f'[NEW CONNECTION] {addr} connected.')
    
    while True:
        conn, addr = server.accept()
        # Create a new thread for each client connection
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print(f"[STARTING] Server is starting on {HOST}:{PORT}...")
start()