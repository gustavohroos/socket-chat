import socket
import threading
from message_handling import create_chat_message, parse_chat_message

host = '127.0.0.1'
port = 12000

clients = []
usernames = set()


def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server.bind((host, port))
        server.listen()
        print("server started!")
    except:
        print("failed to start server!")
        return
    
    while True:
        client, address = server.accept()
        print("connected with {}".format(str(address)))
        clients.append(client)

        # message = create_chat_message("username", "server", 2)
        
        # client.send(message)

        thread = threading.Thread(target=messages_handler, args=(client,))
        thread.start()


def messages_handler(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message.startswith("USERNAME<>"):
                username = message.split("<>")[1]
                broadcast(f"{username} joined!", client)
                usernames.add(username)
                continue
            else:
                broadcast(message, client)
        except:
            delete_client(client)
            break


def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode('utf-8'))
            except:
                print("failed to send message!")
                delete_client(client)


def delete_client(client):
    if client in clients:
        # print("Disconnected with {}".format(str(client)))
        client.close()
        clients.remove(client)

main()