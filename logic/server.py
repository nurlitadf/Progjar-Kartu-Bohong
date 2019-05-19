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
ready_counter = 0
LIE_QUEUE = LifoQueue()


def debug_data(data: dict):
    print('='*20)
    print('======[DEBUG]======')
    for key, val in data.items():
        if isinstance(val, dict):
            print(key)
            for key_, val_ in val.items():
                print(key_, val_)
        else:
            print(key, val)
    print('='*20)


def broadcast(message):
    for client in list_of_clients:
        try:
            client.send(message)
        except Exception as e:
            print(e)
            client.close()
            remove(client)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


def clear_queue():
    global LIE_QUEUE
    while not LIE_QUEUE.empty():
        _, _ = LIE_QUEUE.get()


def make_message(message: str):
    global game
    data = {}
    data['MSG'] = message
    data['GAME'] = game.__dict__
    data = pickle.dumps(data)
    broadcast(data)


def gameplay():
    global game, LIE_QUEUE
    while not game.start:
        pass
    while True:
        while game.state != 'done_pick':
            pass
        game.state = 'lie_or_not'
        # broadcast(pickle.dumps(game.__dict__))
        make_message('choose lie or not')
        while LIE_QUEUE.qsize() < len(game.players):
            pass
        while not LIE_QUEUE.empty():
            name, statement = LIE_QUEUE.get()
            if statement:
                verdict = game.card_placed.check()
                pile = game.card_placed.get_cards()
                if verdict:             # ternyata jujur, tebakan salah
                    victim = name
                    next_turn = game.turn
                else:                   # memang bohong, tebakan benar
                    victim = game.turn
                    next_turn = name
                game.player_decks[victim].extend(pile)
                game.turn = next_turn
                game.state = 'pick'
                # broadcast(pickle.dumps(game.__dict__))


def player_ready():
    global game, ready_counter
    ready_counter += 1
    if ready_counter == 4:
        game.start = True
        game.create_decks()
        game.next_turn()
        broadcast(pickle.dumps(game.__dict__))


def pick_card(message):
    global game
    name = message['NAME']
    if name == game.turn:
        selected = message['SELECTED']
        picked = game.player_decks[name].pick(selected)
        statement = CARD_MAPPING[message['STATEMENT']]
        game.card_placed.add(picked, statement)
        game.state = 'done_pick'
        # broadcast(pickle.dumps(game.__dict__))
        make_message('done pick')


def handle_lie(message):
    global LIE_QUEUE, game
    statement = message['LIE']
    name = message['NAME']
    LIE_QUEUE.put((name, statement))


def client_thread(conn, addr):
    while True:
        try:
            message = conn.recv(BUFFER_SIZE)
            message = pickle.loads(message)
            debug_data(message)
            if message['MSG'] == 'READY':
                player_ready()
            elif message['MSG'] == 'PICK':
                pick_card(message)
            elif message['MSG'] == 'LIE':
                pass

        except:
            remove(conn)


start_new_thread(gameplay, ())
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
        start_new_thread(client_thread, (conn, addr))

        # if len(list_of_clients) == 4:
        #     game.create_decks()
        #     broadcast(pickle.dumps(game.__dict__))

conn.close()
server.close()
