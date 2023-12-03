# Bawa, Francis I.
# Gomez, Zachary R.
# CSNETWK S12 MP
import socket
import json

clients = {}

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific IP address and port
server_address = ('127.0.0.1', 12345)
sock.bind(server_address)

print('Server started at {} port {}'.format(*server_address))

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
            message = {'command': 'error', 'message': 'Error: Command parameters do not match or is not allowed.\n'}
            sock.sendto(json.dumps(message).encode('utf-8'), address)

        else:
            handle = response['params'][0]
            flag = True
            for key, value in clients.items():

                # check if handle is unique
                if key == handle:
                    message = {'command': 'error', 'message': 'Error: Registration failed. Handle or alias already exists.\n'}
                    sock.sendto(json.dumps(message).encode('utf-8'), address)
                    flag = False
                    break

                # check if address is unique
                elif value == address:
                    message = {'command': 'error', 'message': 'Error: Registration failed. Address is already registered.\n'}
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
            message = {'command': 'error', 'message': 'Error: Command parameters do not match or is not allowed.\n'}
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
        pass

    # handle getting of file
    elif response['command'] == '/get':
        pass

    # handle storing of file
    elif response['command'] == '/store':
        pass

    # handle message to single client
    elif response['command'] == '/msg':
        pass

    # handle message to all clients
    elif response['command'] == '/all':
        pass

    # if command does not exist
    else:
        message = {'command': 'error', 'message': 'Error: Command not found.\n'}
        sock.sendto(json.dumps(message).encode('utf-8'), address)


    

