import pickle
import socket
import sys
import time

import pygame
import tkinter
from _thread import start_new_thread
from button import Button

GAME_DATA = {}
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

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1200, 675))

# Ntar ganti biar bagus
green = [39, 102, 23]
screen.fill(green)
pygame.display.set_caption("Kartu Bohong")
ready = Button('assets/button/play.png', 0, 100)
# sampe sini

"""
STATE
1. pick
2. lie_or_not
3. finish
"""

while True:
    pygame.display.flip()
    ready.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONUP:
            if ready.button_clicked():
                make_message("READY")
                break

# Pertama kali terima data state game dari server
data = server.recv(BUFFER_SIZE)
data = pickle.loads(data)
debug_data(data)
GAME_DATA = data['GAME']
MESSAGE = data['MSG']
start_new_thread(receive, ())
num_winner = len(GAME_DATA['winner'])

# Masuk View main game
while True:
    pass
