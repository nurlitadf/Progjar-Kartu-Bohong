import pickle
import socket
import sys

from _thread import start_new_thread


def debug_data(data: dict):
    for key, val in data.items():
        if isinstance(val, dict):
            print(key)
            for key_, val_ in val.items():
                print(key_, val_)
        else:
            print(key, val)


BUFFER_SIZE = 2048

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8081
server.connect((ip_address, port))


data = server.recv(BUFFER_SIZE)

CLIENT_ID = int(data.decode('utf-8'))

name = input("Name>>")
print(name, CLIENT_ID)
server.send(name.encode('utf-8'))

data = server.recv(BUFFER_SIZE)
data = pickle.loads(data)
debug_data(data)


GAME_DATA = {}
GAME_DATA['decks'] = data


def receive():
    global GAME_DATA
    while True:
        data = server.recv(BUFFER_SIZE)
        data = pickle.loads(data)
        GAME_DATA = data
