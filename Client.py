# Bawa, Francis I.
# Gomez, Zachary R.
# CSNETWK S12 MP
import socket
import json
import threading

def send_message(message, server_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serialized_message = json.dumps(message).encode('utf-8')
    client_socket.sendto(serialized_message, server_address)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Welcome")
    print("Enter /? for help")

    while True:
        user_input = input("Enter command: ")
        parts = user_input.split()
        command = parts[0]
        params = parts[1:]

        # show valid commands
        if command == '/?':
            if len(params) == 0:
                print("""Valid Commands:
                        /join <ip> <port> - Join a network
                        /register <username> - Register a user
                        /store <filename> - Store a file
                        /dir - Show a list of all files in the server
                        /get <filename> - Download a file from the server
                        /? - Show this help message
                        """)
            else:
                print("Error: Command parameters do not match or is not allowed.")
            
        elif command == '/join':
            # succesful connection
            if len(params) == 2 and (params[0] =='127.0.0.1' or params[0] == 'localhost') and params[1] == '12345':
                server_address = (params[0], int(params[1]))
                
                sock.connect(server_address)
                # insert rest of code here
            else:
                print("Error: Connection to the Server has failed! Please check IP Address and Port Number.")
        
        elif command == '/leave':
            print("Error: Disconnection failed. Please connect to the server first.")

        else:
            print("Error: Command not found.")
        

if __name__ == "__main__":
    main()