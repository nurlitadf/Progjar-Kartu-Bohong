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
    global GAME_DATA, MESSAGE
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


def render_scoreboard():
    screen.fill(green)
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    f = open("logic/score.txt", "r")
    f1 = f.readlines()
    y=30
    for score in f1:
        textsurface = myfont.render(score[:-1], False, (0, 0, 0))
        screen.blit(textsurface,(30,y))
        y=y+30


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

screen = pygame.display.set_mode((1200, 675))

myfont = pygame.font.SysFont('Comic Sans MS', 24)
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

button_num = []

path = "assets/angka"
hit = 0
for f in os.listdir(path):
    if hit < 7:
        button_num.append(ButtonNumber(os.path.join(path, f), 995 + 28*hit, 575))
    else:
        button_num.append(ButtonNumber(os.path.join(path, f), 995 + 28*(hit%7), 605))
    hit+=1

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

while Flag:
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
            game_status =  "Playing"
    
    elif game_status == "Playing":
        pygame.display.flip()
        #print(GAME_DATA['player_decks']['a'])

        if not game_start:
            game_start = True
            temp = eval(str(GAME_DATA['player_decks'][username]))

            # print(eval(str(my_card_data)))
            # print(type(my_card_data))

            my_card_data = []

            for c in temp:
                c = c.replace('diamond', '1.png')
                c = c.replace('spade', '2.png')
                c = c.replace('heart', '3.png')
                c = c.replace('club', '4.png')

                c = c.lower()

                my_card_data.append(c)

            paths = [os.path.join(path, f) for f in my_card_data]
            pos_my_cards = get_position_my_cards(len(my_card_data))

            my_cards = [Card(paths[i], pos_my_cards[i][0], pos_my_cards[i][1]) for i in range(len(paths))]

        screen.blit(background_main, (0, 0))
        screen.blit(kartu_atas, (510, 0))
        screen.blit(kartu_kiri, (0, 247.5))
        screen.blit(kartu_kanan, (1080, 247.5))

        #draw the buttons
        place_card.draw(screen)
        liar_button.draw(screen)

        for button in button_num:
            button.draw(screen)

        for card in my_cards:
            card.draw(screen)

        for card in active_card:
            card.draw(screen)
        
        for card in middle_card:
            card.draw(screen)

        #print(num_clicked)
        num_text = myfont.render(num_clicked, True, (255, 255, 255))
        screen.blit(num_text,(920,540))



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Flag = False

pygame.quit()
exit(0)

# # num_winner = len(GAME_DATA['winner'])


# # if game_status == "Waiting":
# #         screen.blit(background_waiting, (0, 0))



# #         for event in pygame.event.get():
# #             if event.type == pygame.QUIT:
# #                 pygame.quit()
# #                 exit(0)


# # Masuk View main game
# while True:
#     pass
