import socket

HOST = "127.0.0.1"
PORT = 12346
FORMAT = 'utf-8'
HEADER = 1024



def start():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    
    print(f"[CONNECTED] Connected to server at {HOST}:{PORT}")
    
    while(True):
        
        msg = input("Enter message to send to server: ")
        if msg.lower() == "exit":
            break
    
        while(len(msg) > HEADER):
            print(f"[ERROR] Message too long. Max length is {HEADER} characters.")
            msg = input("Enter message to send to server: ")
        
        msg_len = len(msg)
        send_len = str(msg_len).encode(FORMAT)
        send_len += b' ' * (HEADER - len(send_len))
    
        client.send(send_len)
        client.send(msg.encode(FORMAT))
        print(f"[SENT] {msg} to server")

    client.close()
    print("[DISCONNECTED] Disconnected from server")

print(f"[STARTING] Client is starting...")
start()