import socket

HOST = "127.0.0.1"
PORT = 12360
FORMAT = 'utf-8'
HEADER = 1024


def start():
    client = None
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        
        print(f"[CONNECTED] Connected to server at {HOST}:{PORT}")
        
        while(True):
            
            msg = input("Enter message to send to server: ")
        
            while(len(msg) > HEADER-5):
                print(f"[ERROR] Message too long. Max length is {HEADER-5} characters.")
                msg = input("Enter message to send to server: ")
            
            msg_len = len(msg)
            send_len = str(msg_len).encode(FORMAT)
            send_len += b' ' * (HEADER - len(send_len))
        
            client.send(send_len)
            client.send(msg.encode(FORMAT))
            print(f"[SENT] {msg} to server")

            
            server_msg_len_header = client.recv(HEADER).decode(FORMAT)
            server_msg_len_header = len(server_msg_len_header)
            if server_msg_len_header:
                server_response = client.recv(server_msg_len_header).decode(FORMAT)
                print(f"[SERVER] {server_response}")
            else:
                print("[ERROR] Server closed connection or sent empty data for length.")
            
            if msg.lower() == "exit":
                break

    except ConnectionRefusedError:
        print(f"[ERROR] Connection to {HOST}:{PORT} refused. Is the server running?")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred during client operation: {e}")
    finally:
        if client:
            client.close()
            print("[DISCONNECTED] Disconnected from server (socket closed in finally block)")


print(f"[STARTING] Client is starting...")
start()