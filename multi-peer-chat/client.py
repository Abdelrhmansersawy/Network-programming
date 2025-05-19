import socket
import threading
import time
import sys


# === ANSI Color Codes ===
RED = '\033[91m'
GREEN = '\033[92m'
GRAY = '\033[90m'
RESET = '\033[0m'

def is_server_running(host, port):
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except (ConnectionRefusedError, socket.timeout, OSError):
        return False

def is_port_available(port, host):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_socket:
        return test_socket.connect_ex((host, port)) != 0
     
def register_peer():
    HOST = "127.0.0.1"

    while True:
        try:
            PORT = int(input("Enter the listen port number: "))
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
    print(f"{GREEN}[SUCCESS] Listening on {HOST}:{PORT}{RESET}")

    while True:
        try:
            server_port = int(input("Enter the server port number: "))
            if not (1023 < server_port < 65536):
                print(f"{RED}[ERROR] Port number must be between 1024 and 65535.{RESET}")
                continue
            if not is_server_running(HOST, server_port):
                print(f"{RED}[ERROR] No server running on port {server_port}.{RESET}")
                continue
            break
        except ValueError:
            print(f"{RED}[ERROR] Invalid port number. Please enter a valid integer.{RESET}")
            continue

    print(f"{GRAY}[INFO] Server detected at {HOST}:{server_port}{RESET}")

    peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    peer.connect((HOST, server_port))

    print(f"{GREEN}[SUCCESS] Connected to server at {HOST}:{server_port}{RESET}")
    return peer


def safe_print(message):
    """Prints message safely even during input()."""
    sys.stdout.write('\r' + ' ' * 80 + '\r')  # Clear current line
    print(message)
    sys.stdout.write(f"{GRAY}[PROMPT] Enter your message (or 'q' to quit): {RESET}")
    sys.stdout.flush()
    
def handle_peer(peer):
    def receive_messages():
        try:
            while True:
                data = peer.recv(1024)
                if not data:
                    safe_print(f"{RED}[DISCONNECTED] Server closed the connection.{RESET}")
                    break
                safe_print(f"{GRAY}[RECEIVED] {data.decode().strip()}{RESET}")
        except Exception as e:
            safe_print(f"{RED}[ERROR] Receiving failed: {e}{RESET}")
        finally:
            peer.close()

    def send_messages():
        try:
            while True:
                print(f"{GRAY}[WAIT] Waiting 10 seconds before allowing message input...{RESET}")
                time.sleep(10)
                msg = input(f"{GREEN}[INPUT] Enter your message (or 'q' to quit): {RESET}").strip()
                if msg.lower() == 'q':
                    print(f"{GRAY}[INFO] Quitting...{RESET}")
                    break
                if msg:
                    peer.sendall(msg.encode())
                    print(f"{GREEN}[SENT] {msg}{RESET}")
                else:
                    print(f"{RED}[ERROR] Message cannot be empty.{RESET}")
        except (BrokenPipeError, ConnectionResetError):
            print(f"{RED}[ERROR] Connection lost while sending message.{RESET}")
        except Exception as e:
            print(f"{RED}[ERROR] Unexpected error in sender: {e}{RESET}")
        finally:
            peer.close()

    # Start receiving thread first
    threading.Thread(target=receive_messages, daemon=True).start()
    
    # Start sending in main thread
    send_messages()

    
def start_peer():
    peer = register_peer()
    handle_peer(peer)

if __name__ == "__main__":
    start_peer()
