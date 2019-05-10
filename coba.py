import os
import random

import pygame
from pygame.locals import *

from card import Card
from button import Button

pygame.init()


def start_draw_position(n_cards):
    return (1200 - 20*(n_cards-1) -90)/2 , 20

def draw_cards(paths):
    my_cards = []

    if len(paths) <= 26:
        x_start, space = start_draw_position(len(paths))
        hit = 0

        for p in paths:
            my_cards.append(Card(p, x_start + space*hit, 555))
            hit+=1
    else:
        x_start, space = start_draw_position(len(paths) - 26)
        hit = 0
        
        for i in range(len(paths) - 26):
            my_cards.append(Card(paths[i], x_start + space*hit, 525))
            hit+=1
        
        x_start, space = start_draw_position(26)
        hit = 0

        for i in range(len(paths) - 26, len(paths)):
            my_cards.append(Card(paths[i], x_start + space*hit, 585))
            hit+=1
    
    return my_cards

screen = pygame.display.set_mode((1200, 675))
background = pygame.image.load("assets/bg.jpg")

kartu_kiri = pygame.image.load("assets/kiri.png")
kartu_kanan = pygame.image.load("assets/kanan.png")
kartu_atas = pygame.image.load("assets/atas.png")

buttons = []
buttons.append(Button("assets/pilihangka.png", 1050, 565))
buttons.append(Button("assets/pilihjumlah.png", 1050, 600))
buttons.append(Button("assets/go.png", 1050, 635))
buttons.append(Button("assets/bohong.png", 30, 600))

path = "assets/card"
list_path = [os.path.join(path, f) for f in os.listdir(path)]

#pilih 13 card random
paths = random.sample(list_path, 13)
my_cards = draw_cards(paths)

while(True):
    screen.fill(0)

    #draw the background & cards
    screen.blit(background, (0, 0))
    screen.blit(kartu_atas, (510, 0))
    screen.blit(kartu_kiri, (0, 247.5))
    screen.blit(kartu_kanan, (1080, 247.5))

    #draw the buttons
    for button in buttons:
        button.draw(screen)
    
    for card in my_cards:
        card.draw(screen)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            for c in my_cards:
                c.card_clicked()    

            for b in buttons:
                b.button_clicked(buttons)
                if b.status == 1:
                    if b.name == "pilihangka":
                        print("yes")                

        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
      