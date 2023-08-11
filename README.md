# Simple Chat Server

This is a simple chat server application written in Python. It allows multiple clients to connect and exchange messages in a chat room. The server supports various commands for users, including setting usernames, retrieving user information, and more.

## Chat Message Protocol

This chat defines a structured format for encoding and parsing chat messages in a binary format. This protocol is utilized to facilitate communication between clients and the chat server in a standardized manner, ensuring organized messages that can be easily interpreted by both sender and receiver.

### Message Format

The chat message consists of the following components:

1. **Protocol Version (1 byte):**
   - Indicates the version of the chat message protocol being used.
   - A single byte specifying the protocol version number.

2. **Message Type (4 bytes):**
   - Identifies the purpose or category of the message.
   - A 4-byte integer representing the message type code.
   - Message types are predefined within the application to differentiate between different types of messages (e.g., chat messages, commands, notifications).

3. **Username Length (4 bytes):**
   - Indicates the length (in bytes) of the username being sent.
   - A 4-byte integer specifying the length of the username data.

4. **Message Length (4 bytes):**
   - Indicates the length (in bytes) of the message content.
   - A 4-byte integer specifying the length of the message data.

5. **Username (up to 10 bytes):**
   - The username is encoded as UTF-8 and is a variable-length field, with a maximum of 10 bytes.
   - If the username is shorter than 10 bytes, it is padded with null bytes (0x00) to reach the fixed length.

6. **Timestamp (4 bytes):**
   - Represents the time at which the message was created.
   - A 4-byte integer representing the timestamp value.
   - The timestamp is stored as the number of seconds since the Unix epoch (January 1, 1970).

7. **Message Content (variable length):**
   - The actual content of the chat message.
   - Encoded as UTF-8 and can vary in length based on the message being sent.

### Usage

This protocol ensures that messages are packed into a consistent binary structure, making it efficient for transmission over a network. The provided functions handle the creation and parsing of messages based on this protocol, ensuring that messages are clearly defined and can be reliably processed by the chat application.

## Features

- **Chat messages**: Clients can send and receive chat messages in the chat room.
- **User management**: Users can set their usernames, change usernames, and retrieve user information.
- **Server commands**: Users can issue commands such as quitting the chat, listing users, and pinging the server.
- **Real-time communication**: The server handles real-time communication between clients.

## Prerequisites

Before running the chat server, ensure you have the following installed:

- Python 3.x
- This project does not require any external packages, as it solely relies on Python's built-in modules.

## Usage

1. Clone this repository to your local machine.

2. Run the chat server:

```python server.py```

3. Clients can connect to the server running a suitable client application:

```python client.py```

## Commands

The chat server supports the following commands:

- `/username <new_username>`: Change your username.
- `/users`: List all users in the chat.
- `/user <username>`: Retrieve information about a specific user.
- `/ping`: Ping the server to measure round-trip time (RTT).
- `/quit`: Disconnect from the server and exit the chat.

## TODO
- [ ] End-to-end Encryption
- [ ] Room Creation and Management
- [ ] Account Creation


## Notes

- This is a basic chat server with minimal error handling and security measures.
- The server and client should be running on the same host for testing purposes.
- This application is intended for learning purposes and can be extended for more advanced features and improvements.

## Contributing
Contributions are welcome! If you have any suggestions, bug reports, or would like to contribute code, please feel free to:

- Fork the repository
- Create a new branch
- Make your changes
- Submit a pull request

## Contact
If you have any questions or want to discuss the project, feel free to contact me at [ghroos@inf.ufpel.edu.br](ghroos@inf.ufpel.edu.br).

## Authors

- Gustavo Roos
- Alberto Helbig
- Giordano Rossa

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
