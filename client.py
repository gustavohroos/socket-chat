import socket
import sys
import threading
from message_handling import create_chat_message, parse_chat_message

IP = "127.0.0.1"
PORT = 12000
username = "guest"

def main():
    global username
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server.connect((IP, PORT))
    except:
        print("connection failed!")
        return
    
    while True:
        username = input("please enter your username: ")
        if len(username) > 10:
            print("username too long!")
            continue
        break
    print("connected!")

    receive_thread = threading.Thread(target=receive_messages, args=(server,))
    send_thread = threading.Thread(target=send_messages, args=(server, username,))

    receive_thread.start()
    send_thread.start()

def receive_messages(server):
    while True:
        try:
            message = server.recv(2048)
            message = parse_chat_message(message)
            
            if message["type"] == 2:
                if message["content"] == "username":
                    response = create_chat_message(username, username, 2)
                    server.send(f"USERNAME<>{username}".encode('utf-8'))
                    continue

            print(message + '\n')

        except:
            server.close()
            sys.exit()

def send_messages(server, username):
    while True:
        try:
            message = input('\n')
            if message.startswith("/"):
                if message == "/quit":
                    print("disconnecting!")
                    raise
                elif message.startswith("/username"):
                    if len(message.split()) < 2:
                        print("Use /username new_username!")
                        continue
                    if len(message.split()[1]) > 10:
                        print("Username too long!")
                        continue
                    if username == message.split()[1]:
                        print("You already have that username!")
                        continue
                    if message.split()[1] in username:
                        print("Username cannot contain spaces!")
                        continue
                    if message.split()[1] == "server":
                        print("You cannot have that username!")
                        continue
                    old_username = username
                    username = message.split()[1]
                    server.send(f"{old_username} changed username to {username}".encode('utf-8'))
                    continue
                elif message == "/help":
                    print("\ncommands:")
                    print("\n/quit - disconnect from server")
                    print("/username <new_username> - change username")
                    continue
                else:
                    print("unknown command! type /help for help!")
                    continue

            server.send(f'< {username} > {message}'.encode('utf-8'))
            # client.send(create_chat_message(f'< {username} > {message}'))

        except:
            server.close()
            sys.exit()

main()