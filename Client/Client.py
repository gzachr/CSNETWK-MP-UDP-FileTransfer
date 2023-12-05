# Bawa, Francis I.
# Gomez, Zachary R.
# CSNETWK S12 MP
import socket
import json
import threading
import os

server_address = None
is_registered = False

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

def receive_file(file_name):
    try:
        with open(file_name, 'wb') as file:
            while True:
                data, addr = client_socket.recvfrom(1024)

                if not data:
                    break

                file.write(data)
            
            file.close()
            print(f"File received from Server: {file_name}\n")
    
    except Exception as e:
        print(f"Error: {e}\n")

# receive messages from server
def receive_response():
    global server_address
    global is_registered

    while True:
        # if server_address is not None:
        try:
            data, addr = client_socket.recvfrom(1024)

            response = json.loads(data.decode())

            if response['command'] == 'join' or response['command'] == 'error' or response['command'] == 'store':
                print(f"{response['message']}\n")
            
            elif response['command'] == 'leave':
                print(f"{response['message']}\n")
                server_address = None
                is_registered = False  
            
            elif response['command'] == 'register':
                is_registered = True
                print(f"Welcome {response['client']}!")
                print(f"{response['message']}\n")

            elif response['command'] == 'msg':
                print(f"{response['handle']}: {response['message']}\n")

            elif response['command'] == 'all':
                print(f"{response['handle']}: {response['message']}\n")
            
            elif response['command'] == 'dir':
                print(f'{response["message"]}')
                
                if len(response['files']) > 0:
                    for file in response['files']:
                        print(f'\t{file}')
                    
                    print('\n')
                else:
                    print('\tNo files stored on the server.\n')
            
            elif response['command'] == 'get':
                receive_file(response['file_name'])

        except ConnectionResetError:
            print("Error: Connection Failed")
        
def start():
    count = 0
    while True:
        
        global server_address

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
            if server_address:
                print('Error: You are already connected to the server.\n')
            elif len(params) == 2 and (params[0] =='127.0.0.1' or params[0] == 'localhost') and params[1] == '12345':
                
                temp = (params[0], int(params[1]))
                client_socket.sendto(json.dumps(message).encode('utf-8'), temp)

                if count == 0:
                    receive_thread = threading.Thread(target=receive_response)
                    receive_thread.start()
        

                server_address = temp
                count += 1
            else:
                print('Error: Connection to the Server has failed! Please check IP Address and Port Number.\n')
        
        elif command == '/register' or command == '/get' or command == '/dir' or command == '/msg' or command == '/all':
            if server_address:
                client_socket.sendto(json.dumps(message).encode('utf-8'), server_address)
            else:
                print('Error: Please connect to the server first.\n')
        
        elif command == '/store':
            if server_address:
                if is_registered:
                    if len(params) == 1:
                        if os.path.isfile(params[0]):
                            try:
                                with open(params[0], 'rb') as file:
                                    client_socket.sendto(json.dumps(message).encode('utf-8'), server_address)
                                    file_data = file.read(1024)

                                    while file_data:
                                        client_socket.sendto(file_data, server_address)
                                        file_data = file.read(1024)
                                    
                                    # send empty data packet to signify end of transfer
                                    client_socket.sendto(b'', server_address)
                                    
                            except Exception as e:
                                print(f"Error: {e}")
                        else:
                            print('Error: File not found.\n')
                    else:
                        print('Error: Command parameters do not match or is not allowed.\n')
                else:
                    print('Error: Register a unique handle/alias first.\n')
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

print("Input /? to view possible commands")
print("Enter command: ")
start()