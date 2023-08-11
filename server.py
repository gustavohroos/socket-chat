import socket
import threading
import json
import time

from message_handling import create_chat_message, parse_chat_message
from message_types import MessageTypes  # Assuming you have a separate message_types.py file

host = '127.0.0.1'
port = 12000

clients = []
server = None
usernames = {}

event = threading.Event()


def main():
    global server
    global event

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server.bind((host, port))
        server.listen()
        print("server started!")

        check_if_has_users_thread = threading.Thread(target=check_if_has_users, args=(event,))
        check_if_has_users_thread.start()
    except Exception as e:
        print("failed to start server: ", str(e))
        return
    
    while True:
        try:
            if event.is_set():
                break
            client, address = server.accept()
            print(f"connected with {str(address)}")
            clients.append(client)

            user_thread = threading.Thread(target=messages_handler, args=(event, client,))
            user_thread.start()
        except Exception as e:
            print("error accepting connection: ", str(e))


def check_if_has_users(event):
    while True:
        if event.is_set():
            break
        if len(clients) == 0:
            print("waiting for users...")
        time.sleep(1)


def messages_handler(event, client):
    while True:
        try:
            if event.is_set():
                break
            raw_message = client.recv(2048)
            message = parse_chat_message(raw_message)

            if message["message_type"] == MessageTypes.CHAT_MESSAGE:
                broadcast(raw_message, client)
                continue

            if message["message_type"] == MessageTypes.SET_USERNAME_COMMAND:
                username = message["content"]
                if username in usernames.values():
                    response = create_chat_message("", "server", MessageTypes.ERROR_JOINING_CHAT)
                    client.send(response)
                    continue

                usernames[client] = username
                response = create_chat_message("", "server", MessageTypes.SUCCESS_JOINING_CHAT)
                client.send(response)
                response = create_chat_message(f'{username} joined!', "server", MessageTypes.JOIN_MESSAGE)
                broadcast(response, client)
                continue

            if message["message_type"] == MessageTypes.GET_USERINFO_COMMAND:
                username = message["content"]
                user_address = get_client_by_username(username)
                if user_address is None:
                    response = create_chat_message("", "server", MessageTypes.RETRIEVE_USER_INFO)
                    client.send(response)
                    continue
                response = str((username,) + user_address)
                response = create_chat_message(response, "server", MessageTypes.RETRIEVE_USER_INFO)
                client.send(response)
                continue

            if message["message_type"] == MessageTypes.CHANGE_USERNAME_COMMAND:
                new_username = message["content"]
                old_username = message["username"]
                if new_username in usernames.values():
                    response = create_chat_message("", "server", MessageTypes.ERROR_SETTING_USERNAME)
                    client.send(response)
                    continue

                usernames[client] = new_username
                response = create_chat_message(new_username, "server", MessageTypes.SUCCESS_SETTING_USERNAME)
                client.send(response)
                response = create_chat_message(f"user '{old_username}' changed username to '{new_username}'!", "server", MessageTypes.USER_CHANGED_USERNAME_MESSAGE)
                broadcast(response, client)
                continue

            if message["message_type"] == MessageTypes.GET_USERS_COMMAND:
                users = [username for username in usernames.values()]
                response = create_chat_message(str(users), "server", MessageTypes.USERS_LIST_MESSAGE)
                client.send(response)
                continue

            if message["message_type"] == MessageTypes.QUIT_COMMAND:
                response = create_chat_message("", "server", MessageTypes.SUCCESS_QUITTING_CHAT)
                client.send(response)
                message = create_chat_message(f'{usernames[client]} left!', "server", MessageTypes.LEAVE_MESSAGE)
                broadcast(message, client)
                delete_client(client)
                break

            if message["message_type"] == MessageTypes.PING_REQUEST:
                response = create_chat_message(str(time.time()), "server", MessageTypes.PONG_RESPONSE)
                client.send(response)
                continue

            print(json.dumps(message, indent=4))
            print("unknown message type!")
            continue
        except Exception as e:
            print(e)
            print("failed to receive message!")
            message = create_chat_message(f'{usernames[client]} left!', "server", MessageTypes.LEAVE_MESSAGE)
            broadcast(message, client)
            delete_client(client)
            break


def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except Exception as e:
                print(e)
                print("failed to send message!")
                delete_client(client)


def get_client_by_username(target_username):
    global usernames
    for client, username in usernames.items():
        if username == target_username:
            return client.getpeername()
    return None


def delete_client(client):
    if client in clients:
        client.close()
        clients.remove(client)
        del usernames[client]


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("server stopped!")
        event.set()
        for client in clients:
            client.close()
        server.close()