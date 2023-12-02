# Bawa, Francis I.
# Gomez, Zachary R.
# CSNETWK S12 MP
import socket
import json
import threading

server_address = None
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_message(sock, message, server_address):
    serialized_message = json.dumps(message).encode('utf-8')
    sock.sendto(serialized_message, server_address)

def handle_response():
    while True:
        data = sock.recvfrom(1024)
        message = json.loads(data.decode())

        print(f"{message['message']}")

def send_commands():
    is_registered = False

    while True:
        user_input = input("Enter command => ")
        parts = user_input.split()
        command = parts[0]
        params = parts[1:]

        message = {'command': command, 'params': params}

        if command == '/register':
            if len(params) == 1:
                if is_registered:
                    print("Error: You are already registered.\n")
                else:
                    send
            else:
                print("Error: Command parameters do not match or is not allowed.\n")



def display_commands():
    print("""\nValid Commands:
            /join <ip> <port> - Join a network
            /register <username> - Register a user
            /store <filename> - Store a file
            /dir - Show a list of all files in the server
            /get <filename> - Download a file from the server
            /? - Show this help message
            """)

def main():
    print("Welcome")
    print("Enter /? for help")

    while True:
        user_input = input("Enter command => ")
        parts = user_input.split()
        command = parts[0]
        params = parts[1:]

        # show valid commands
        if command == '/?':
            if len(params) == 0:
                display_commands()
            else:
                print("Error: Command parameters do not match or is not allowed.\n")
            
        elif command == '/join':
            # succesful connection
            if len(params) == 2 and (params[0] =='127.0.0.1' or params[0] == 'localhost') and params[1] == '12345':
                server_address = (params[0], int(params[1]))
                
                sock.connect(server_address)
                print("Connected to the server.")

                # thread for handling responses from server
                response_thread = threading.Thread(target=handle_response)
                # thread for handling user input
                send_thread = threading.Thread(target=send_commands)

                response_thread.start()
                send_thread.start()
              
            else:
                print("Error: Connection to the Server has failed! Please check IP Address and Port Number.\n")
        
        elif command == '/register':
            print("Error: Please connect to the server first.\n")
        elif command == '/store':
            print("Error: Please connect to the server first.\n")
        elif command == '/dir':
            print("Error: Please connect to the server first.\n")
        elif command == '/get':
            print("Error: Please connect to the server first.\n")
        elif command == '/leave':
            print("Error: Disconnection failed. Please connect to the server first.\n")

        else:
            print("Error: Command not found.\n")
        

if __name__ == "__main__":
    main()