import socket
import threading
import os
from colorama import init, Fore

os.system('cls')

def receive_messages(socket):
    while True:
        try:
            data = socket.recv(1024)
            if not data:
                break
            received_message = data.decode()
            split_message = received_message.split(" ")
            if split_message[0] == '!attach':
                file = open(f'C:\\Users\\Liron\\Desktop\\peerchat\\received\\{split_message[1]}', 'wb')
                while True:
                    image_chunk = socket.recv(1024)
                    if image_chunk == b'!attach_end':
                        break
                    file.write(image_chunk)
                file.close()
                print(f"{Fore.CYAN}attachment received: {split_message[1]}{Fore.RESET}")
            else:
                print(f"{Fore.BLUE}[PEER] {received_message}{Fore.RESET}")


        except Exception as e:
            print(f"Error while receiving: {str(e)}")
            break

def send_messages(socket):
    while True:
        message = input()
        split_message = message.split(' ')
        if split_message[0] == '!attach':
            socket.send(message.encode())
            file = open(f'C:\\Users\\Liron\\Desktop\\peerchat\\{split_message[1]}', 'rb')
            data = file.read(1024)
            while data:
                socket.send(data)
                data = file.read(1024)
            file.close()
            socket.send(b'!attach_end')
        else:
            try:
                socket.send(message.encode())
            except Exception as e:
                print(f"Error while sending: {str(e)}")
                break

def peer_init():
    PEER_ADDRESS = 'localhost'
    PEER_PORT = 12344 + int(input("Enter peer's port: "))
    return PEER_ADDRESS, PEER_PORT

def cli_init():
    CLI_ADDRESS = 'localhost'
    CLI_PORT = 12344 + int(input("Enter your port: "))
    return CLI_ADDRESS, CLI_PORT

def connect_peers():
    print(f"Attempting to connect to {PEER}...")
    while True:
        try:
            CLI_SOCKET.connect(PEER)
            print(f"{Fore.GREEN}~ CONNECTION ESTABLISHED ~{Fore.RESET}")
            break
        except Exception as E:
            pass

PEER = peer_init()
CLI = cli_init()

# print(f'{Fore.BLUE}PEER{Fore.RESET}', PEER, "CLI", CLI)

CLI_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLI_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
CLI_SOCKET.bind(CLI)

connect_peers()

# Create the threads
send_thread = threading.Thread(target=send_messages, args=(CLI_SOCKET,))
receive_thread = threading.Thread(target=receive_messages, args=(CLI_SOCKET,))

# Start the threads
receive_thread.start()
send_thread.start()

# Wait for both threads to finish (you can use Ctrl+C to stop the application)
receive_thread.join()
send_thread.join()
