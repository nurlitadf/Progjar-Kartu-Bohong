import os
import random

import pygame
from pygame.locals import *


class Card(object):
    def __init__(self, path, x, y):
        self.image = pygame.image.load(path).convert_alpha()
        self.path = path
        self.num = path.split('-')[0]
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.status = 0 #0 tidak aktif, 1 aktif (naik ke atas), 2 dipilih buat ditaruh di tengah

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def move(self, speedx, speedy):
        self.rect.x += speedx
        self.rect.y += speedy

    def card_clicked(self):
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]

        if (mouse_x >= self.rect.x + 15) & (mouse_x <= self.rect.x + 30): 
            if (mouse_y >= self.rect.y + 15) & (mouse_y <= self.rect.y + 70):
                if self.status == 0:
                    self.move(0, -40)
                    self.status = 1
                elif self.status == 1 :
                    self.move(0, 40)
                    self.status = 0


def start_draw_position(n_cards):
    return (960 - 20*(n_cards-1) -90)/2 , 20

pygame.init()
screen = pygame.display.set_mode((960, 540))

background = pygame.image.load("assets/bg.jpg")

kartu_kiri = pygame.image.load("assets/kiri.png")
kartu_kanan = pygame.image.load("assets/kanan.png")
kartu_atas = pygame.image.load("assets/atas.png")

pilih_angka = pygame.image.load("assets/pilihangka.png")
pilih_jumlah = pygame.image.load("assets/pilihjumlah.png")
go_button = pygame.image.load("assets/go.png")
bohong_button = pygame.image.load("assets/bohong.png")

path = "assets/card"
list_path = [os.path.join(path, f) for f in os.listdir(path)]

#pilih 13 card random
paths = random.sample(list_path, 13)
my_cards = []

if len(paths) <= 26:
    x_start, space = start_draw_position(len(paths))
    hit = 0

    for p in paths:
        my_cards.append(Card(p, x_start + space*hit, 420))
        hit+=1
else:
    x_start, space = start_draw_position(len(paths) - 26)
    hit = 0
    
    for i in range(len(paths) - 26):
        my_cards.append(Card(paths[i], x_start + space*hit, 390))
        hit+=1
    
    x_start, space = start_draw_position(26)
    hit = 0

    for i in range(len(paths) - 26, len(paths)):
        my_cards.append(Card(paths[i], x_start + space*hit, 450))
        hit+=1
    

while(True):
    screen.fill(0)

    #draw the background & cards
    screen.blit(background, (0, 0))
    screen.blit(kartu_atas, (390, 0))
    screen.blit(kartu_kiri, (0, 180))
    screen.blit(kartu_kanan, (840, 180))

    #draw the button
    screen.blit(pilih_angka, (810, 430))
    screen.blit(pilih_jumlah, (810, 465))
    screen.blit(go_button, (810, 500))
    screen.blit(bohong_button, (30, 465))

    for card in my_cards:
        card.draw()        

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            for c in my_cards:
                c.card_clicked()    


        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)