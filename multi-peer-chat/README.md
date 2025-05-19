# Multi-Peer Chat Application

## Description

This project implements a simple multi-peer chat application using Python's `socket` and `threading` libraries. It consists of a central server that relays messages between multiple connected clients. Clients can send messages to the server, which then broadcasts them to all other connected clients.

## Features

### Server (`server.py`)
-   Listens for incoming client connections on a user-specified port.
-   Handles multiple client connections concurrently using threading.
-   Broadcasts messages received from one client to all other connected clients.
-   Manages a list of connected peers and their addresses.
-   Provides console output for server status, new connections, received messages, and disconnections.
-   Gracefully handles client disconnections.
-   Uses ANSI color codes for enhanced console output readability.

### Client (`client.py`)
-   Connects to the central server at a user-specified host and port.
-   Allows the user to specify a local "listening" port (though it primarily acts as an outgoing connector).
-   Verifies if the chosen local port is available and if the target server is running.
-   Sends messages to the server.
-   Receives and displays messages broadcast by the server from other clients.
-   Uses threading to handle sending and receiving messages simultaneously, allowing for non-blocking I/O.
-   Includes a `safe_print` function to ensure messages are displayed correctly without interfering with user input.
-   Provides console output for connection status, sent/received messages, and errors.
-   Uses ANSI color codes for enhanced console output readability.
-   Allows the user to quit the chat by typing 'q'.

## Requirements

-   Python 3.x

No external libraries are required beyond standard Python modules.

## How to Run

### 1. Start the Server

Open a terminal and navigate to the project directory. Run the server script:
```bash
python server.py
```
The server will prompt you to enter a port number. For example, if you enter `8080`:
```
Enter the port number: 8080
[SUCCESS] Server started on 127.0.0.1:8080
```

### 2. Start the Client(s)

Open one or more new terminal windows and navigate to the project directory. Run the client script:
```bash
python client.py
```
Each client will prompt you to:
1.  Enter a listen port number (e.g., `5000`).
2.  Enter the server port number (the port the server is listening on, e.g., `8080`).

Example client startup:
```
Enter the listen port number: 5000
[SUCCESS] Listening on 127.0.0.1:5000
Enter the server port number: 8080
[INFO] Server detected at 127.0.0.1:8080
[SUCCESS] Connected to server at 127.0.0.1:8080
[WAIT] Waiting 10 seconds before allowing message input...
```

## Usage

Once a client is connected to the server:
-   After the initial 10-second wait, the client will prompt: `[INPUT] Enter your message (or 'q' to quit):`
-   To send a message: Type your message and press Enter.
-   To quit: Type `q` and press Enter.
-   Messages from other clients will appear in your terminal, prefixed with `[RECEIVED]`.

### Example Chat Session

Let's assume the server is running on port `8080`.

**Client 1 Terminal:**
```
Enter the listen port number: 5001
[SUCCESS] Listening on 127.0.0.1:5001
Enter the server port number: 8080
[INFO] Server detected at 127.0.0.1:8080
[SUCCESS] Connected to server at 127.0.0.1:8080
[WAIT] Waiting 10 seconds before allowing message input...
[INPUT] Enter your message (or 'q' to quit): Hello from Client 1!
[SENT] Hello from Client 1!
                                                                                
[RECEIVED] Hello from Client 2!
[INPUT] Enter your message (or 'q' to quit): q
[INFO] Quitting...
```

**Client 2 Terminal:**
```
Enter the listen port number: 5002
[SUCCESS] Listening on 127.0.0.1:5002
Enter the server port number: 8080
[INFO] Server detected at 127.0.0.1:8080
[SUCCESS] Connected to server at 127.0.0.1:8080
[WAIT] Waiting 10 seconds before allowing message input...
                                                                                
[RECEIVED] Hello from Client 1!
[INPUT] Enter your message (or 'q' to quit): Hello from Client 2!
[SENT] Hello from Client 2!
[INPUT] Enter your message (or 'q' to quit): 
```

**Server Terminal Output:**
```
Enter the port number: 8080
[SUCCESS] Server started on 127.0.0.1:8080
[NEW CONNECTION] Peer 127.0.0.1:XXXXX connected.
[ACTIVE CONNECTIONS] 1
[NEW CONNECTION] Peer 127.0.0.1:YYYYY connected.
[ACTIVE CONNECTIONS] 2
[RECEIVED] From 127.0.0.1:XXXXX: Hello from Client 1!
[RECEIVED] From 127.0.0.1:YYYYY: Hello from Client 2!
[CONNECTION RESET] Peer 127.0.0.1:XXXXX forcibly closed the connection. // When Client 1 quits
[DISCONNECTED] 127.0.0.1:XXXXX removed from peers list.
// Server continues running, waiting for more connections or messages from Client 2
```

The server terminal will display logs of connections, disconnections, and messages being relayed. 