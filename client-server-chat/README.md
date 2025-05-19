# Client-Server Chat Application

This project implements a simple client-server chat application using Python's `socket` and `threading` libraries.

## Description

The application allows multiple clients to connect to a central server and exchange messages. The server listens for incoming connections and handles each client in a separate thread. Messages are sent with a fixed-size header that indicates the length of the upcoming message.

## Features

-   **Server**:
    -   Listens for client connections on a specified host and port (`127.0.0.1:12360` by default).
    -   Handles multiple clients concurrently using threading.
    -   Receives messages from clients and sends back a confirmation ("Message received by server").
    -   Recognizes an "exit" command from the client to close the connection.
    -   Prints connection status, received messages, and errors to the console.
-   **Client**:
    -   Connects to the server at a specified host and port.
    -   Allows the user to input messages to send to the server.
    -   Validates message length against a predefined header size.
    -   Sends messages to the server and prints the server's response.
    -   Sends an "exit" command to the server to terminate the connection.
    -   Prints connection status, sent messages, server responses, and errors to the console.

## Protocol

The client and server communicate using a simple protocol:
1.  **Message Length Header**: Before sending the actual message, the sender (client or server) first sends a header of a fixed size (defined by `HEADER`, default 1024 bytes).
2.  This header contains the length of the upcoming message, encoded in the specified `FORMAT` (default 'utf-8'), and padded with spaces to fill the `HEADER` size.
3.  **Message Data**: After sending the header, the sender transmits the actual message, encoded in the specified `FORMAT`.
4.  The receiver first reads the header to determine the length of the incoming message and then reads that many bytes for the message content.

## How to Run

### Prerequisites

-   Python 3.x

### 1. Start the Server

Open a terminal and navigate to the project directory. Run the server script:

```bash
python server.py
```

The server will start listening for connections. You should see output like:
```
[STARTING] Server is starting...
[LISTENING] Server is listening on 127.0.0.1:12360
```

### 2. Start the Client

Open another terminal (or multiple terminals for multiple clients) and navigate to the project directory. Run the client script:

```bash
python client.py
```

The client will attempt to connect to the server. If successful, you should see:
```
[STARTING] Client is starting...
[CONNECTED] Connected to server at 127.0.0.1:12360
```
You can then start sending messages from the client terminal.

**Example Client Interaction:**
```
Enter message to send to server: Hello Server!
[SENT] Hello Server! to server
[SERVER] Message received by server
Enter message to send to server: exit
[SENT] exit to server
[SERVER] Goodbye!
[DISCONNECTED] Disconnected from server (socket closed in finally block)
```

**Corresponding Server Output:**
```
[NEW CONNECTION] ('127.0.0.1', <some_port_number>) connected.
[ACTIVE CONNECTIONS] 1
[('127.0.0.1', <some_port_number>)] Received: Hello Server!
[('127.0.0.1', <some_port_number>)] Sent response: 'Message received by server'
[('127.0.0.1', <some_port_number>)] Received: exit
[DISCONNECTING] ('127.0.0.1', <some_port_number>) sent exit command.
[('127.0.0.1', <some_port_number>)] Sent response: 'Goodbye!'
[DISCONNECTED] ('127.0.0.1', <some_port_number>) disconnected.
[ACTIVE CONNECTIONS] 0
```

## Configuration

The host, port, header size, and encoding format can be configured by changing the global variables at the top of `client.py` and `server.py`:

-   `HOST`: The IP address for the server to bind to and for the client to connect to (default: "127.0.0.1").
-   `PORT`: The port number for communication (default: 12360).
-   `HEADER`: The size of the message length header in bytes (default: 1024). **Ensure this is the same in both client.py and server.py.**
-   `FORMAT`: The encoding format for messages (default: 'utf-8'). **Ensure this is the same in both client.py and server.py.**
