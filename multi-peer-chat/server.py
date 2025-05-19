import socket
import threading

# === ANSI Color Codes ===
RED = '\033[91m'
GREEN = '\033[92m'
GRAY = '\033[90m'
RESET = '\033[0m'

peers = []
peer_addresses = {}
lock = threading.Lock()  # To avoid race conditions

def broadcast_message(message, sender_conn):
    with lock:
        for peer in peers.copy():
            if peer != sender_conn:
                try:
                    peer.send(message.encode('utf-8'))
                except Exception as e:
                    peer_str = peer_addresses.get(peer, "Unknown")
                    print(f"{RED}[ERROR] Could not send message to {peer_str}: {e}{RESET}")
                    
                    peers.remove(peer)
                    peer_addresses.pop(peer, None)
                    print(f"{RED}[DISCONNECTED] {peer_str} removed from peers list.{RESET}")

def handle_client(conn, addr):
    peer_str = f"{addr[0]}:{addr[1]}"
    print(f"{GREEN}[NEW CONNECTION] Peer {peer_str} connected.{RESET}")

    with lock:
        peers.append(conn)
        peer_addresses[conn] = peer_str

    try:
        while True:
            msg = conn.recv(1024)
            if not msg:
                break
            msg = msg.decode('utf-8')
            print(f"{GREEN}[RECEIVED] From {peer_str}: {msg}{RESET}")
            broadcast_message(msg, conn)
    except ConnectionResetError:
        print(f"{RED}[CONNECTION RESET] Peer {peer_str} forcibly closed the connection.{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR] Unexpected issue with peer {peer_str}: {e}{RESET}")
    finally:
        with lock:
            if conn in peers:
                peers.remove(conn)
            peer_addresses.pop(conn, None)
        conn.close()

def is_port_available(port, host):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_socket:
        return test_socket.connect_ex((host, port)) != 0

def broadcast_server():
    HOST = "127.0.0.1"

    while True:
        try:
            PORT = int(input("Enter the port number: "))
            if not (1023 < PORT < 65536):
                print(f"{RED}[ERROR] Port number must be between 1024 and 65535.{RESET}")
                continue
            if not is_port_available(PORT, HOST):
                print(f"{RED}[ERROR] Port {PORT} is already in use. Please choose another port.{RESET}")
                continue
            break
        except ValueError:
            print(f"{RED}[ERROR] Invalid port number. Please enter a valid integer.{RESET}")
            continue

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))

    print(f"{GREEN}[SUCCESS] Server started on {HOST}:{PORT}{RESET}")
    return server

def start_server():
    server = broadcast_server()
    server.listen()
    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
            print(f"{GRAY}[ACTIVE CONNECTIONS] {threading.active_count() - 1}{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR] Error accepting connection: {e}{RESET}")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
