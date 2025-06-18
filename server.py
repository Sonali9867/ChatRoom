import socket
import threading


HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = []



def listen_for_messages(client, username):
    while 1:
        try:
            message = client.recv(2048).decode('utf-8')

            if message:
                if message.startswith("__left__:"):
                    left_username = message.split(":")[1]
                    active_clients.remove((left_username, client))
                    send_messages_to_all(f"~~~{left_username} has left the chat~~~")
                    client.close()
                    break
                else:
                    final_message = username + ' : ' + message
                    send_messages_to_all(final_message)
            else:
                print(f"Message sent from client {username} is empty.")
        except:
            
            if (username, client) in active_clients:
                active_clients.remove((username, client))
                send_messages_to_all(f"~~~~{username} has left the chat~~~~")
            client.close()
            break


#Function to send message to a specific client
def send_message_to_one_client(client,message):
    client.sendall(message.encode())


#Function to send message to all the clients
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_one_client(user[1],message)


def client_handler(client):
    while 1:

        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username,client))
            prompt_message = f"~~~{username} has joined the chat~~~"   
            send_messages_to_all(prompt_message)
            break

        else:
            print("Username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()
    


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #IPv4 and TCP is used for communication

    try:
        server.bind((HOST,PORT))
        print(f"Running the server ON {HOST} {PORT}")
    except:
        print("Unable to bind to host {HOST} and port {PORT}")

    server.listen(LISTENER_LIMIT)

    while 1:
        client, address = server.accept()  
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler,args=(client, )).start()

if __name__=='__main__':
    main()