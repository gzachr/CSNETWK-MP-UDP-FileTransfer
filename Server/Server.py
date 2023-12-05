# Bawa, Francis I.
# Gomez, Zachary R.
# CSNETWK S12 MP
import socket
import json
import os
from datetime import datetime

# dictionary of clients
clients = {}

# get list of files in current directory
current_dir = os.getcwd()
current_dir = current_dir + '\Files'
files = os.listdir(current_dir)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific IP address and port
server_address = ('127.0.0.1', 12345)
sock.bind(server_address)

print('Server started at {} port {}'.format(*server_address))

def receive_file(file_name):
    global current_dir
    file_path = os.path.join(current_dir, file_name)
    try:
        with open(file_path, 'wb') as file:
            print('Receiving file...')

            while True:
                data, address = sock.recvfrom(1024)
                if not data:
                    break
                file.write(data)
            
            file.close()
            print('File received.')
            return True
        
    except FileNotFoundError:
        print(f'Error: {e}')
        return False

while True:
    data, address = sock.recvfrom(1024)

    try:
        response = json.loads(data.decode())
    
    except json.JSONDecodeError as e:
        message = {'command': 'error', 'message': str(e)}
        sock.sendto(json.dumps(message).encode('utf-8'), address)
        continue

    # handle joining
    if response['command'] == '/join':
        print(f"Client {address} connected to server")
        message = {'command': 'join', 'message': "Connection to the File Exchange Server is successful!"}
        sock.sendto(json.dumps(message).encode('utf-8'), address)


    # handle registration
    elif response['command'] == '/register':
        # check num of params
        if len(response['params']) != 1:
            message = {'command': 'error', 'message': 'Error: Command parameters do not match or is not allowed.'}
            sock.sendto(json.dumps(message).encode('utf-8'), address)

        else:
            handle = response['params'][0]
            flag = True
            for key, value in clients.items():

                # check if handle is unique
                if key == handle:
                    message = {'command': 'error', 'message': 'Error: Registration failed. Handle or alias already exists.'}
                    sock.sendto(json.dumps(message).encode('utf-8'), address)
                    flag = False
                    break

                # check if address is unique
                elif value == address:
                    message = {'command': 'error', 'message': 'Error: Registration failed. Address is already registered.'}
                    sock.sendto(json.dumps(message).encode('utf-8'), address)
                    flag = False
                    break

            # register handle           
            if flag:
                clients[handle] = address
                print(f"Client {address} registered as {handle}")
                message = {'command': 'register', 'client':  handle, 'message': 'You have successfully registered.'}
                sock.sendto(json.dumps(message).encode('utf-8'), address)
        
        print(clients)
    

    # handle leaving
    elif response['command'] == '/leave':
        # check num of params
        if len(response['params']) != 0:
            message = {'command': 'error', 'message': 'Error: Command parameters do not match or is not allowed.'}
            sock.sendto(json.dumps(message).encode('utf-8'), address)

        else:
            # remove client from list if registered
            for key, value in clients.items():
                if value == address:
                    print(f"Client {key} left the server")
                    clients.pop(key)
                    break

            # notify client of disconnection
            print(f"{address} has disconnected")
            message = {'command': 'leave', 'message': f"Connection closed. Thank you!"}
            sock.sendto(json.dumps(message).encode('utf-8'), address)
    

    # handle list of files (dir)
    elif response['command'] == '/dir':
        #check num of params
        if len(response['params']) != 0:
            message = {'command': 'error', 'message': 'Error: Command parameters do not match or is not allowed.'}
            sock.sendto(json.dumps(message).encode('utf-8'), address)
        
        #check if registered
        else:
            for key, value in clients.items():
                if value == address:
                    message = {'command': 'dir', 'files': files, 'message': 'Server Directory'}
                    sock.sendto(json.dumps(message).encode('utf-8'), address)
                    break
            
            # notify that user is unregistered
            else:
                message = {'command': 'error', 'message': "Error: Register a unique handle/alias first."}
                sock.sendto(json.dumps(message).encode('utf-8'), address)


    # handle getting of file
    elif response['command'] == '/get':
        flag = True

        # check num of params
        if len(response['params']) != 1:
            message = {'command': 'error', 'message': 'Error: Command parameters do not match or is not allowed.'}
            sock.sendto(json.dumps(message).encode('utf-8'), address)
        
        # check if registered
        for key, value in clients.items():
            if value == address:
                flag = False
                file_name = response['params'][0]

                # check if file exists
                if file_name in files:
                    file_path = os.path.join(current_dir, file_name)
                    try:
                        with open(file_path, 'rb') as file:
                            print('Sending file...')

                            message = {'command': 'get', 'file_name': file_name}
                            sock.sendto(json.dumps(message).encode('utf-8'), address)
                            data = file.read(1024)

                            while data:
                                sock.sendto(data, address)
                                data = file.read(1024)
                            
                            file.close()

                            # send empty data packet to signify end of transfer
                            sock.sendto(b'', address)
                            print('File sent.')

                    except Exception as e:
                        message = {'command': 'error', 'message': f'Error: {e}'}
                        sock.sendto(json.dumps(message).encode('utf-8'), address)
                else:
                    message = {'command': 'error', 'message': "Error: Error: File not found in the server."}
                    sock.sendto(json.dumps(message).encode('utf-8'), address)  
                break
        
        if flag:
            message = {'command': 'error', 'message': "Error: Register a unique handle/alias first."}
            sock.sendto(json.dumps(message).encode('utf-8'), address)

    # handle storing of file
    elif response['command'] == '/store':
        flag = True
        
        for key, value in clients.items():
            if value == address:
                handle = key
            
                file_name = response['params'][0]
                files.append(file_name)
                result = receive_file(file_name)

                if result:
                    formatted_time = datetime.now().strftime("<%Y-%m-%d %H:%M:%S>")
                    message = {'command': 'store', 'message': f"{handle}{formatted_time}: Uploaded {file_name}"}
                    sock.sendto(json.dumps(message).encode('utf-8'), address)
                else:
                    message = {'command': 'error', 'message': "Error: File not successfully stored."}
                    sock.sendto(json.dumps(message).encode('utf-8'), address)
                
                flag = False
                break

        # notify that user is unregistered
        if flag:
            message = {'command': 'error', 'message': "Error: Register a unique handle/alias first."}
            sock.sendto(json.dumps(message).encode('utf-8'), address)


    # handle message to single client
    elif response['command'] == '/msg':
        user_handle = None
       
        for key, value in clients.items():
            if value == address:
                user_handle = key

        if user_handle == None:
            message = {'command': 'error', 'handle': user_handle, 'message': "Register a unique handle/alias first."}
            sock.sendto(json.dumps(message).encode('utf-8'), address)
        else:
            if len(response['params']) < 2:
                message = {'command': 'error', 'handle': user_handle, 'message': 'Error: Command parameters do not match or is not allowed.\n'}
                sock.sendto(json.dumps(message).encode('utf-8'), address)
            else:
                target = response['params'].pop(0)

                if target != user_handle:
                    if target in clients.keys():
                        for key, value in clients.items():
                            if target == key:
                                response = ' '.join(response['params'])
                                message = {'command': 'msg', 'handle': user_handle, 'message': response}
                                sock.sendto(json.dumps(message).encode('utf-8'), value)
                                break
                    else:
                        message = {'command': 'error', 'handle': user_handle, 'message': 'There is no user with that handle, please doublecheck your input.\n'}
                        sock.sendto(json.dumps(message).encode('utf-8'), address)
                else:
                    message = {'command': 'error', 'handle': user_handle, 'message': 'You cannot send a message to yourself.\n'}
                    sock.sendto(json.dumps(message).encode('utf-8'), address)


    # handle message to all clients
    elif response['command'] == '/all':
        user_handle = None
       
        for key, value in clients.items():
            if value == address:
                user_handle = key

        if user_handle == None:
            message = {'command': 'error', 'handle': user_handle, 'message': "Register a unique handle/alias first."}
            sock.sendto(json.dumps(message).encode('utf-8'), address)
        else:
            if len(response['params']) == 0:
                message = {'command': 'error', 'handle': user_handle, 'message': 'Error: Command parameters do not match or is not allowed.\n'}
                sock.sendto(json.dumps(message).encode('utf-8'), address)

            else:
                response = ' '.join(response['params'])
                message = {'command': 'all', 'handle': user_handle, 'message': response}

                for value in clients.values():
                    sock.sendto(json.dumps(message).encode('utf-8'), value)
        

    # if command does not exist
    else:
        message = {'command': 'error', 'message': 'Error: Command not found.'}
        sock.sendto(json.dumps(message).encode('utf-8'), address)


    

