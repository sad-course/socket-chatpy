import socket
import threading

def receive_message(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            print('Received from server: ' + data)  
        except:
            client_socket.close()
            break

def run_client_program():
    port = 8090 

    name = input("Enter your name: ")
    while not name:
        print("Name cannot be empty.")
        name = input("Enter your name: ")


    client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    
    client_socket.sendall(b'client_name' + name.encode())

    threading.Thread(target=receive_message, args=(client_socket,)).start()
    print("Connected to server. Type 'bye' to exit.")

    message = input(" -> ")

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())
        message = input(" -> ")

    client_socket.close


if __name__ == '__main__':
    run_client_program()