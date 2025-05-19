import socket
import threading

HOST = "127.0.0.1"
PORT = 12360

HEADER = 1024
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    try:
        while connected:
            msg_length_header = conn.recv(HEADER)
            if not msg_length_header:
                print(f"[DISCONNECTED] {addr} closed connection unexpectedly (empty header).")
                break
            
            msg_length_str = msg_length_header.decode(FORMAT)
            msg_length = int(msg_length_str)

            if msg_length:
                msg_bytes = conn.recv(msg_length)
                
                msg = msg_bytes.decode(FORMAT)
                print(f"[{addr}] Received: {msg}")

                if msg.lower() == "exit":
                    print(f"[DISCONNECTING] {addr} sent exit command.")
                    response_str = "Goodbye!"
                    connected = False
                else:
                    response_str = "Message received by server"
                
                response_bytes = response_str.encode(FORMAT)
                
                response_len_header = str(len(response_bytes)).encode(FORMAT)
                response_len_header += b' ' * (HEADER - len(response_len_header))
                
                conn.sendall(response_len_header)
                conn.sendall(response_bytes) 
                print(f"[{addr}] Sent response: '{response_str}'")
            else:
                print(f"[INFO] {addr} sent a message with length 0.")


    except ConnectionResetError:
        print(f"[CONNECTION RESET] {addr} connection reset by peer.")
    except Exception as e:
        print(f"[ERROR] Unexpected error with client {addr}: {e}")
    finally:
        print(f"[DISCONNECTED] {addr} disconnected.")
        conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    
    while True:
        try:
            conn, addr = server.accept()

            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        except Exception as e:
            print(f"[ERROR] Error accepting connection: {e}")


print(f"[STARTING] Server is starting...")
start()