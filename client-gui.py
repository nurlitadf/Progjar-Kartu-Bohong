import pickle
import socket
import sys
import time
import os

import pygame
import tkinter
from _thread import start_new_thread

from button import *
from card import *
from utils import *

from component import VAL_TO_CARD

GAME_DATA = None
MESSAGE = ""
BUFFER_SIZE = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8081
server.connect((ip_address, port))

data = server.recv(BUFFER_SIZE)
CLIENT_ID = int(data.decode('utf-8'))
print(CLIENT_ID)


def get_input():
    global input_username, root, username, server
    username = input_username.get()
    server.send(username.encode('utf-8'))
    root.destroy()


def make_message(message, **kwargs):
    data = {}
    data['ID'] = CLIENT_ID
    data['NAME'] = username
    data['MSG'] = message
    data.update(kwargs)
    print(data)
    data = pickle.dumps(data)
    server.send(data)


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


def receive():
    global GAME_DATA, MESSAGE, my_cards, username, path, paths, middle_card, active_card
    while True:
        data = server.recv(BUFFER_SIZE)
        data = pickle.loads(data)
        debug_data(data)
        MESSAGE = data['MSG']
        if(MESSAGE == "DONE"):
            print("Ranking:")
            print(data['WINNER'])
            print("Scoreboard:")
            print(data['SCOREBOARD'])
        GAME_DATA = data['GAME']

        temp = eval(str(GAME_DATA['player_decks'][username]))

        my_card_data = []

        for c in temp:
            c = c.replace('diamond', '1.png')
            c = c.replace('spade', '2.png')
            c = c.replace('heart', '3.png')
            c = c.replace('club', '4.png')

            my_card_data.append(c)

        paths = [os.path.join(path, f) for f in my_card_data]
        pos_my_cards = get_position_my_cards(len(my_card_data))

        my_cards = [Card(paths[i], pos_my_cards[i][0], pos_my_cards[i][1]) for i in range(len(paths))]

        temp = len(GAME_DATA['card_placed']) - len(active_card)

        # print("-------------------------", temp)

        middle_card = []

        for i in range(temp):
            middle_card.append(Card("assets/x.png", 450, 300-i*3))



def render_scoreboard():
    global screen

    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    f = open("score.txt", "r")
    f1 = f.readlines()
    y = 30
    for score in f1:
        textsurface = myfont.render(score[:-1], False, (0, 0, 0))
        screen.blit(textsurface, (30, y))
        y = y+30


root = tkinter.Tk()
root.title('Input Your Username')

tkinter.Label(root, text="Username:     ").grid(row=0)
input_username = tkinter.Entry(root)
input_username.focus_set()

input_username.grid(row=0, column=1)

tkinter.Button(root, text='Play', command=get_input).grid(row=2, column=1)

username = ""

root.mainloop()
game_status = "Ready"

pygame.init()
pygame.font.init()
pygame.display.set_caption("Kartu Bohong - Player {}".format(username))

screen = pygame.display.set_mode((1200, 675))

myfont = pygame.font.SysFont('Comic Sans MS', 24)
background_score = pygame.image.load("assets/bg.jpg")
background_ready = pygame.image.load("assets/bg0.jpg")
background_waiting = pygame.image.load("assets/bg1.jpg")
background_main = pygame.image.load("assets/bg2.jpg")

button_ready = Button('assets/button/play.png', 625, 300)
game_start = False

kartu_kiri = pygame.image.load("assets/kiri.png")
kartu_kanan = pygame.image.load("assets/kanan.png")
kartu_atas = pygame.image.load("assets/atas.png")

place_card = Button("assets/placecard.png", 1087, 537)
liar_button = Button("assets/liar.png", 100, 550)
honest_button = Button("assets/honest_.png", 220, 550)
button_num = []

path = "assets/angka"
hit = 0
for f in os.listdir(path):
    if hit < 7:
        button_num.append(ButtonNumber(os.path.join(path, f), 995 + 28*hit, 575))
    else:
        button_num.append(ButtonNumber(os.path.join(path, f), 995 + 28*(hit % 7), 605))
    hit += 1

path = "assets/card"
#list_path = [os.path.join(path, f) for f in os.listdir(path)]

paths = None
pos_my_cards = None
my_cards = []

num_clicked = "0"

middle_card = []
hit_middle = 0
active_card = []

"""
STATE
1. pick
2. lie_or_not
3. finish
"""

start_new_thread(receive, ())
Flag = True
has_click_lie_or_not = False

console_message = ""
state_now = ""


while Flag:
    if GAME_DATA is not None and (username in GAME_DATA['winner']):
        screen.blit(background_score, (0, 0))
        render_scoreboard()

    if game_status == "Ready":
        pygame.display.flip()
        screen.blit(background_ready, (0, 0))
        button_ready.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Flag = False

            if event.type == pygame.MOUSEBUTTONUP:
                if button_ready.button_clicked():
                    make_message("READY")
                    del button_ready

                    game_status = "Waiting"

    elif game_status == "Waiting":
        pygame.display.flip()
        screen.blit(background_waiting, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Flag = False

        if GAME_DATA is not None:
            game_status = "Playing"

    elif game_status == "Playing":
        pygame.display.flip()
        # print(GAME_DATA['player_decks']['a'])

        if GAME_DATA['state'] != 'lie_or_not':
            has_click_lie_or_not = False

        screen.blit(background_main, (0, 0))
        screen.blit(kartu_atas, (510, 0))
        screen.blit(kartu_kiri, (0, 247.5))
        screen.blit(kartu_kanan, (1080, 247.5))

        # draw the buttons
        if GAME_DATA['turn'] == username and GAME_DATA['state'] == 'pick':
            place_card.draw(screen)
        if GAME_DATA['turn'] != username and GAME_DATA['state'] == 'lie_or_not':
            liar_button.draw(screen)
            honest_button.draw(screen)

        if GAME_DATA['turn'] == username and GAME_DATA['state'] == 'pick':
            for button in button_num:
                button.draw(screen)

        for card in my_cards:
            card.draw(screen)

        for card in active_card:
            card.draw(screen)

        for card in middle_card:
            card.draw(screen)

        if username not in GAME_DATA['winner']:
            if (GAME_DATA['state'] == 'pick'):
                turn = "It's Player {} Turn".format(GAME_DATA['turn'])
                console_turn = myfont.render(turn, True, (255, 255, 255))
                screen.blit(console_turn, (30, 30))


                if username == GAME_DATA['turn']:
                    if not GAME_DATA['card_placed'].is_empty():
                        num_cards = len(GAME_DATA['card_placed'])
                        last_val = VAL_TO_CARD[GAME_DATA['card_placed'].values[-1]]

                        console_message = '[Curently there are {} cards of {}]'.format(num_cards, last_val)
                    else:
                        console_message = ""
                
                else:
                    console_message = "Now {} is picking cards".format(GAME_DATA['turn'])
                    for c in active_card[:]:
                       active_card.remove(c)
                       del c

                    active_card = []

                console_txt = myfont.render(console_message, True, (255, 255, 255))
                screen.blit(console_txt, (30, 60))
        
        if GAME_DATA['state'] == 'lie_or_not':
            if username != GAME_DATA['turn']:
                num_card = len(GAME_DATA['card_placed'].cards[-1])
                card_name = VAL_TO_CARD[GAME_DATA['card_placed'].values[-1]]
                msg = "player {} put {} {} cards".format(
                    GAME_DATA['turn'],
                    num_card,
                    card_name
                )
                console_message = msg
            else:
                console_message = "Wait for other players"
            
            console_txt = myfont.render(console_message, True, (255, 255, 255))
            screen.blit(console_txt, (30, 60))

            

        # print(num_clicked)
        if GAME_DATA['turn'] == username and GAME_DATA['state'] == 'pick':
            if GAME_DATA['previous_card'] is not None:
                num_clicked = GAME_DATA['previous_card']
            num_text = myfont.render(num_clicked, True, (255, 255, 255))
            screen.blit(num_text, (920, 540))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                for c in my_cards:
                    c.card_clicked()

                if place_card.button_clicked():

                    active_card = []
                    hit = 0

                    active_card_idx = []

                    for i in range(len(my_cards)):
                        if my_cards[i].status == 1:
                            active_card_idx.append(i)

                    for c in my_cards[:]:
                        if(c.status == 1):
                            active_card.append(CardPlaced(c.path, 550 + hit*80, 300))
                            hit+=1

                    if len(active_card_idx) > 0:
                        if GAME_DATA['previous_card'] is not None:
                            num_clicked = GAME_DATA['previous_card']
                        make_message('PICK', SELECTED=active_card_idx, STATEMENT=num_clicked)

                if honest_button.button_clicked() and not has_click_lie_or_not:
                    print("honest")
                    has_click_lie_or_not = True
                    make_message('LIE', LIE=False)

                if liar_button.button_clicked() and not has_click_lie_or_not:
                    print("liar button")
                    has_click_lie_or_not = True
                    make_message('LIE', LIE=True)
                    

                if GAME_DATA['previous_card'] is None:
                    for b in button_num:
                        flag, num = b.button_clicked()
                        if flag:
                            num_clicked = num

            if event.type == pygame.QUIT:
                Flag = False

pygame.quit()
exit(0)
