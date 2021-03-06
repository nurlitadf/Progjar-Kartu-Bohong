import pickle
import socket
import sys
import time

import pygame
import tkinter
from _thread import start_new_thread
from button import Button

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
        screen.blit(background_main, (0, 0))

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
