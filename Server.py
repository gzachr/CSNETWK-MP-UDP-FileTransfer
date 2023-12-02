# Bawa, Francis I.
# Gomez, Zachary R.
# CSNETWK S12 MP
import socket
import json

server_ip = '127.0.0.1'
server_port = 12345

def send_message(message, server_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serialized_message = json.dumps(message).encode('utf-8')
    client_socket.sendto(serialized_message, server_address)

# handles the /join command
def join(params, addr):
    pass

# handles the /register command
def register(params, addr):
    pass

# handles the /store command
def store(params, addr):
    pass

# handles the /dir command
def dir(params, addr):
    pass

# handles the /get command
def get(params, addr):
    pass

# handles the /? command
def help(params, addr):
    pass



command_list = {
    '/join': join,
    '/register': register,
     '/store': store,
     '/dir': dir,
     '/get': get,
     '/?': help,
}

def parse_message(message_str):
    message = json.loads(message_str)
    return message["command"], message["params"]

def main():
    #UDP socket
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((server_ip, server_port))

    print("Server is listening on {}, Port:{}".format(server_ip, server_port))

    while True:
        data, addr = sock.recvfrom(1024)
        message_str = data.decode('utf-8')
        command, message = parse_message(message_str)

        if command == '/join':
            message = {"head": "join", "message": "You are already connected to the server"}
            send_message(message, addr)

        else:
            send_message({'message': 'Error: Command not found.'}, addr)
        
if __name__ == "__main__":
    main()

