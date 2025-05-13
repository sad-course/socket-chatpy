import socket
import sys
import threading

socket_clients = {}

def connect_socket_client(conn, address):
    
    def thread_func():
        initial_data = conn.recv(1024).decode()
        if initial_data.startswith('client_name'):
            client_name = initial_data.split('client_name')[1]
            print("Client name: " + str(client_name))
        
        socket_clients.update({client_name: {"conn": conn, "address": address}})
        print("Um teste")
        print(socket_clients)
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            
            print("Client connected" + str(address) + ": " + str(data))

            if data.startswith('client_name'):
                pass
            else:
                for client in socket_clients.items():
                    connection = client["conn"]
                    if connection != conn:
                        print("Sending to client " + str(client["address"]))
                        connection.send(data.encode())
                    
            if data.lower() == 'bye':
                print("Client " + str(address) + " disconnected")
                conn.close()
                socket_clients.remove(client)
                break
        conn.close()
        
    return threading.Thread(target=thread_func, args=())

def run_server(clients_count):
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) #SOCK_DGRAM for UDP # get instance

    server_socket.bind(('localhost', 8090))

    while clients_count > 0:
        print('Server listening to connections... ')
        server_socket.listen(clients_count)
        conn, address = server_socket.accept()
        thread_ = connect_socket_client(conn, address)
        thread_.start()
        clients_count -= 1

if __name__ == '__main__':
    run_server(int(sys.argv[1]))