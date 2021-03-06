import pickle
import random
import socket
import sys
import time
from queue import Queue

from _thread import start_new_thread
from component import CARD_MAPPING, Card, CardPlaced, Deck, VAL_TO_CARD
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
LIE_QUEUE = Queue()

NAME_TO_ID = {}
ID_TO_NAME = {}


def debug_data(data: dict):
    print('='*20)
    print('======[DEBUG]======')

    def recur(data: dict):
        for key, val in data.items():
            if isinstance(val, dict):
                print(key)
                recur(val)
            else:
                print(key, val)
    recur(data)
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
    # debug_data(data)
    debug_data(game.__dict__)
    broadcast(data)


def player_ready():
    global game, ready_counter
    ready_counter += 1
    if ready_counter == 4:  # INI DIUBAH JADI 4
        time.sleep(1)
        game.start = True
        game.create_decks()
        game.check_quad_deck()
        game.next_turn()
        game.state = 'pick'
        # debug_data(game.__dict__)
        make_message("START")


def pick_card(message):
    global game
    name = message['NAME']
    if name == game.turn:
        selected = message['SELECTED']
        picked = game.player_decks[name].pick(selected)
        statement = CARD_MAPPING[message['STATEMENT']]
        game.card_placed.add(picked, statement)
        game.state = 'done_pick'


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
                handle_lie(message)

        except:
            remove(conn)


def is_game_over():
    if(game.is_everyone_win()):
        for player in game.players:
            if not game.player_decks[player].empty():
                game.winner.append(player)
        game.update_score()
        game.state = 'finish'
        game.finish = True
        winner = {}
        winner['MSG'] = "DONE"
        winner['WINNER'] = game.winner
        winner['SCOREBOARD'] = game.sorted_score_list
        winner['GAME'] = game.__dict__
        winner = pickle.dumps(winner)
        broadcast(winner)
        time.sleep(2)
        sys.exit(0)


def lie_or_not_phase():
    global game, LIE_QUEUE
    while LIE_QUEUE.qsize() < len(game.players) - len(game.winner) - 1:
        # print(LIE_QUEUE.qsize())
        time.sleep(0.5)
        pass
    while not LIE_QUEUE.empty():
        name, statement = LIE_QUEUE.get()
        if statement:
            clear_queue()
            verdict = game.card_placed.check()
            recently_placed_cards = game.card_placed.cards[-1]
            pile = game.card_placed.get_cards()
            if verdict:             # ternyata jujur, tebakan salah
                victim = name
                next_turn = game.turn
            else:                   # memang bohong, tebakan benar
                victim = game.turn
                next_turn = name
            if verdict:
                msg = "Player {} guess is wrong, player {} is honest, player {}'s cards are ".format(
                    name, game.turn, game.turn)
            else:
                msg = "Player {} guess is correct, player {} is liar, player {}'s cards are ".format(
                    name, game.turn, game.turn)
            for card in recently_placed_cards:
                msg = msg+str(card)+" "
            game.previous_card = None
            game.is_someone_win(game.turn)
            game.player_decks[victim].extend(pile)
            game.check_quad_deck()
            if next_turn in game.winner:
                game.next_turn()
            else:
                game.turn = next_turn
            game.state = 'pick'
            make_message(msg)
            is_game_over()
            return
    game.previous_card = VAL_TO_CARD[game.card_placed.values[-1]]
    game.is_someone_win(game.turn)
    is_game_over()
    game.state = 'pick'
    game.next_turn()
    make_message("CONTINUE")


def gameplay():
    global game, LIE_QUEUE
    while not game.start:
        pass
    while True:
        print('[PICK]')
        while game.state != 'done_pick':
            pass
        print('[LIE OR NOT]')
        game.state = 'lie_or_not'
        make_message('choose lie or not')
        lie_or_not_phase()


start_new_thread(gameplay, ())
while True:
    if len(list_of_clients) < 4:  # INI DIUBAH KE 4
        conn, addr = server.accept()
        list_of_clients.append(conn)
        print(addr[0] + " connected")
        conn.send(str(len(list_of_clients)).encode('utf-8'))
        name = conn.recv(BUFFER_SIZE).decode('utf-8')

        NAME_TO_ID[name] = len(list_of_clients)
        ID_TO_NAME[len(list_of_clients)] = name

        game.add_players(name)
        list_of_name.append(name)
        print(name, len(list_of_clients))
        start_new_thread(client_thread, (conn, addr))

conn.close()
server.close()
