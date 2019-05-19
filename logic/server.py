import pickle
import random
import socket
import sys
from queue import LifoQueue

from _thread import start_new_thread
from component import CARD_MAPPING, Card, CardPlaced, Deck
from game import Game

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_ADDRESS = '127.0.0.1'
PORT = 8081
BUFFER_SIZE = 2048
server.bind((IP_ADDRESS, PORT))
server.listen(100)

list_of_clients = []
list_of_name = []
game = Game()


def debug_data(data: dict):
    for key, val in data.items():
        if isinstance(val, dict):
            print(key)
            for key_, val_ in val.items():
                print(key_, val_)
        else:
            print(key, val)


def broadcast(message, connection):
    for client in list_of_clients:
        try:
            client.send(message)
        except:
            client.close()
            remove(client)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


def create_decks(names: list):
    decks = []
    for suit in ['spade', 'heart', 'diamond', 'club']:
        for name in list(range(2, 11)) + ['J', 'Q', 'K', 'A']:
            decks.append([str(name), suit])
    random.shuffle(decks)

    player_decks = {}
    for i, player in enumerate(names):
        temp_deck = decks[i * 13:(i + 1) * 13]
        new_deck = Deck()
        for card in temp_deck:
            new_deck.add(Card(card[0], card[1]))
        player_decks[player] = new_deck
    return player_decks


while True:
    if len(list_of_clients) < 4:
        conn, addr = server.accept()
        list_of_clients.append(conn)
        print(addr[0] + " connected")
        conn.send(str(len(list_of_clients)).encode('utf-8'))
        name = conn.recv(BUFFER_SIZE).decode('utf-8')
        game.add_players(name)
        list_of_name.append(name)
        print(name, len(list_of_clients))
        # start_new_thread(client_thread, (conn, addr))

        if len(list_of_clients) == 4:
            game.create_decks()
            player_decks = create_decks(list_of_name)
            debug_data(player_decks)
            player_decks = pickle.dumps(player_decks)
            broadcast(player_decks, server)

conn.close()
server.close()
