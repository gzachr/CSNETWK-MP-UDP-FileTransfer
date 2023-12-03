# Bawa, Francis I.
# Gomez, Zachary R.
# CSNETWK S12 MP
import socket
import json
import threading

server_address = None

def display_commands():
    print('\nValid Commands:')
    print('/? - Display commands')
    print('/join <server address> - Join a server')
    print('/register <handle> - Register a handle to the serer')
    print('/store <filename> - Store a file')
    print('/get <filename> - Retrieve a file from the server')
    print('/dir - List all stored files on the server')
    print('/msg <handle> <message> - Send a message to a client')
    print('/all <message> - Send a message to all clients')
    print('/leave - Leave the server\n')

# receive messages from server
def receive_response():
    global server_address

    while True:
        if server_address is not None:
            try:
                data, addr = client_socket.recvfrom(1024)

                if not data:
                    break

                response = json.loads(data.decode())

                if response['command'] == 'join' or response['command'] == 'error':
                        print(f"{response['message']}\n")
                
                elif response['command'] == 'leave':
                    print(f"{response['message']}\n")
                    server_address = None  
                
                elif response['command'] == 'register':
                    print(f"Welcome {response['client']}!")
                    print(f"{response['message']}\n")

                # do message based on other responses
            
            except json.JSONDecodeError:
                print('Error decoding JSON data from the server.\n')
        

def start():
    while True:
        user_input = input()
        parts = user_input.split()
        command = parts[0]
        params = parts[1:]

        message = {'command': command, 'params': params}

        if command == '/?':
            if len(params) == 0:
                display_commands()
            else:
                print('Error: Command parameters do not match or is not allowed.\n')

        elif command == '/join':
            if len(params) == 2 and (params[0] =='127.0.0.1' or params[0] == 'localhost') and params[1] == '12345':
                temp = (params[0], int(params[1]))
                client_socket.sendto(json.dumps(message).encode('utf-8'), temp)

                global server_address 
                server_address = temp
            else:
                print('Error: Connection to the Server has failed! Please check IP Address and Port Number.\n')
        
        elif command == '/register' or command == '/store' or command == '/get' or command == '/dir' or command == '/msg' or command == '/all':
            if server_address:
                client_socket.sendto(json.dumps(message).encode('utf-8'), server_address)
            else:
                print('Error: Please connect to the server first.\n')
        
        elif command == '/leave':
            if server_address:
                client_socket.sendto(json.dumps(message).encode('utf-8'), server_address)
            else:
                print('Error: Disconnection failed. Please connect to the server first.\n')
        
        else:
            print('Error: Command not found.\n')

# UDP Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#threads
receive_thread = threading.Thread(target=receive_response)

receive_thread.start()

print("Input /? to view possible commands")
print("Enter command: ")
start()

    
