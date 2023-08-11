import socket
import sys
import threading
import ast
import time

from message_handling import create_chat_message, parse_chat_message
from message_types import MessageTypes

IP = "127.0.0.1"
PORT = 12000
my_username = "guest"

wait = True

def main():
    global my_username
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server.connect((IP, PORT))
    except:
        print("connection failed!")
        return

    receive_thread = threading.Thread(target=receive_messages, args=(server,))
    send_thread = threading.Thread(target=send_messages, args=(server,))

    receive_thread.start()
    send_thread.start()

def receive_messages(server):
    global my_username
    while True:
        try:
            message = server.recv(2048)
            message = parse_chat_message(message)

            if message["message_type"] in (MessageTypes.CHAT_MESSAGE, MessageTypes.SERVER_MESSAGE,
                                          MessageTypes.JOIN_MESSAGE, MessageTypes.LEAVE_MESSAGE,
                                          MessageTypes.USER_CHANGED_USERNAME_MESSAGE):
                print(f'\n< {message["username"]} - {message["timestamp"]} > {message["content"]}\n')
                continue

            if message["message_type"] in (MessageTypes.ERROR_SETTING_USERNAME, MessageTypes.ERROR_JOINING_CHAT):
                print("username already in use!\n")
                continue

            if message["message_type"] == MessageTypes.SUCCESS_SETTING_USERNAME:
                my_username = message["content"]
                print(f"username set to {my_username}!\n")
                continue

            if message["message_type"] == MessageTypes.SUCCESS_JOINING_CHAT:
                print("joined chat!\nnow you can type...")
                global wait
                wait = False
                continue

            if message["message_type"] == MessageTypes.SUCCESS_QUITTING_CHAT:
                print("disconnecting...")
                server.close()
                sys.exit()

            if message["message_type"] == MessageTypes.RETRIEVE_USER_INFO:
                if message["content"] == "":
                    print("user not found!\n")
                    continue
                user_tuple = ast.literal_eval(message["content"])
                username, ip, port = user_tuple
                print("user info:")
                print(f"username: {username}\nip: {ip}\nport: {port}\n")
                continue

            if message["message_type"] == MessageTypes.PONG_RESPONSE:
                time_sent_by_client = float(message["content"])
                time_received_by_client = float(time.time())
                rtt = (time_received_by_client - time_sent_by_client) * 1000  # Convert to milliseconds
                print(f"< {message['username']} > pong! rtt: {rtt:.3f} ms\n")
                continue

            if message["message_type"] == MessageTypes.USERS_LIST_MESSAGE:
                users = ast.literal_eval(message["content"])
                print("users in chat:")
                for user in users:
                    print("> ", user)
                print()
                continue

            print(message)
            print("unknown message type!")
            print(f'\n< {message["username"]} - {message["timestamp"]} > {message["content"]}\n')
            continue

        except IOError as e:
            print(e)
            server.close()
            sys.exit()

def send_messages(server):
    global my_username

    while wait == True:
        while True:
            my_username = input("please enter your username: ")
            if len(my_username) > 10:
                print("username too long!")
                continue
            break
        message = create_chat_message(my_username, my_username, MessageTypes.SET_USERNAME_COMMAND)
        server.send(message)
        time.sleep(0.1)

    while True:
        try:
            message = input('\n')

            if message.startswith("/"):

                if message == "/quit":
                    server.send(create_chat_message("", my_username, MessageTypes.QUIT_COMMAND))
                    break

                if message.startswith("/username"):
                    if len(message.split()) < 2:
                        print("use /username new_username!\n")
                        continue
                    if len(message.split()[1]) > 10:
                        print("username too long!\n")
                        continue
                    if my_username == message.split()[1]:
                        print("you already have that username!\n")
                        continue
                    if " " in message.split()[1:]:
                        print("username cannot contain spaces!\n")
                        continue
                    if message.split()[1].lower() == "server":
                        print("you cannot have that username!\n")
                        continue

                    new_username = message.split()[1]
                    message = create_chat_message(new_username, my_username, MessageTypes.CHANGE_USERNAME_COMMAND)
                    server.send(message)
                    continue


                if message == "/help":
                    print("\ncommands:")
                    print("/quit - disconnect from server")
                    print("/username <new_username> - change username")
                    print("/users - get list of users")
                    print("/user <username> - get user information")
                    print("/ping - ping the server (not implemented)")
                    continue

                if message == "/users":
                    message = create_chat_message("", my_username, MessageTypes.GET_USERS_COMMAND)
                    server.send(message)
                    continue

                if message.startswith("/user"):
                    splited_message = message.split()
                    if splited_message[1] == "server":
                        print("you cannot get information about the server!\n")
                        continue
                    if len(splited_message) != 2:
                        print("use /user <username>!\n")
                        continue
                    if len(splited_message[1]) > 10:
                        print("username too long!\n")
                        continue

                    message = create_chat_message(splited_message[1], my_username, MessageTypes.GET_USERINFO_COMMAND)
                    server.send(message)
                    continue

                if message == "/ping":
                    message = create_chat_message(str(time.time()), my_username, MessageTypes.PING_REQUEST)
                    server.send(message)
                    continue

                else:
                    print("unknown command! type /help for help!")
                    continue

            response = create_chat_message(message, my_username, MessageTypes.CHAT_MESSAGE)
            server.send(response)

        except IOError as e:
            print(e)
            print("disconnected from server!")
            message = create_chat_message("", my_username, MessageTypes.QUIT_COMMAND)
            server.send(message)
            server.close()
            break

def set_username():

    while True:
        new_username = input("enter your username: ")
        if len(new_username) > 10:
            print("username too long!")
            continue
        if " " in new_username:
            print("username cannot contain spaces!")
            continue
        if new_username == "server":
            print("you cannot have that username!")
            continue
        if new_username == my_username:
            print("you already have that username!")
            continue
        break

    return new_username

if __name__ == '__main__':
    main()
