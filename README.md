# Simple Chat Server

This is a simple chat server application written in Python. It allows multiple clients to connect and exchange messages in a chat room. The server supports various commands for users, including setting usernames, retrieving user information, and more.

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
If you have any questions or want to discuss the project, feel free to contact me at [ghroos@inf.ufpel.edu.br].

## Authors

- [Gustavo Roos]
- [Alberto Helbig]
- [Giordano Rossa]

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
