import os
import random

import tkinter
import pygame
from pygame.locals import *

from utils import *

from card import *
from button import *

def get_input():
    global input_username, root, username
    username = input_username.get()
    root.destroy()

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

myfont = pygame.font.SysFont('Comic Sans MS', 24)

print(username)

screen = pygame.display.set_mode((1200, 675))
background = pygame.image.load("assets/bg2.jpg")

kartu_kiri = pygame.image.load("assets/kiri.png")
kartu_kanan = pygame.image.load("assets/kanan.png")
kartu_atas = pygame.image.load("assets/atas.png")

place_card = Button("assets/placecard.png", 1087, 537)
liar_button = Button("assets/liar.png", 100, 550)

button_num = []
button_amount = []

path = "assets/angka"
hit = 0
for f in os.listdir(path):
    if hit < 7:
        button_num.append(ButtonNumber(os.path.join(path, f), 995 + 28*hit, 575))
    else:
        button_num.append(ButtonNumber(os.path.join(path, f), 995 + 28*(hit%7), 605))
    hit+=1

path = "assets/jumlah"
hit = 0
for f in os.listdir(path):
    button_amount.append(ButtonAmount(os.path.join(path, f), 995 + 28*hit, 640))
    hit+=1

path = "assets/card"
list_path = [os.path.join(path, f) for f in os.listdir(path)]

#pilih 13 card random
paths = random.sample(list_path, 13)
print(paths)
pos_my_cards = get_position_my_cards(13)

my_cards = [Card(paths[i], pos_my_cards[i][0], pos_my_cards[i][1]) for i in range(len(paths))]


num_clicked = "0"
amount_clicked = "0"

middle_card = []
hit_middle = 0
active_card = []

while(True):

    pygame.display.flip()
    screen.fill(0)

    #draw the background & cards
    screen.blit(background, (0, 0))
    screen.blit(kartu_atas, (510, 0))
    screen.blit(kartu_kiri, (0, 247.5))
    screen.blit(kartu_kanan, (1080, 247.5))

    #draw the buttons
    place_card.draw(screen)
    liar_button.draw(screen)

    for button in button_num:
        button.draw(screen)
    
    for button in button_amount:
        button.draw(screen)
    
    for card in my_cards:
        card.draw(screen)

    for card in active_card:
        card.draw(screen)
    
    for card in middle_card:
        card.draw(screen)
    
    #print(num_clicked)
    num_text = myfont.render(num_clicked, True, (255, 255, 255))
    amount_text = myfont.render(amount_clicked, True, (255, 255, 255))

    screen.blit(num_text,(920,540))
    screen.blit(amount_text,(960,540))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            for c in my_cards:
                c.card_clicked()

            if place_card.button_clicked():
                for c in active_card:
                    c.to_stack(450, 300-hit_middle*3)
                    middle_card.append(c)

                    hit_middle+=1

                active_card = []
                
                hit = 0

                for c in my_cards[:]:
                    if(c.status == 1):
                        active_card.append(CardPlaced(c.path, 550 + hit*80, 300))
                    
                        my_cards.remove(c)
                        paths.remove(c.path)
                        del c

                        hit+=1
            
            if liar_button.button_clicked():
                print("liar button")
                for c in active_card:
                    middle_card.append(c)

                active_card = []

                for c in middle_card[:]:
                    paths.append(c.path)
                    middle_card.remove(c)
                    del c

                pos_my_cards = get_position_my_cards(len(paths))
                del my_cards
                my_cards = []

                for i in range(len(paths)):
                    my_cards.append(Card(paths[i], pos_my_cards[i][0], pos_my_cards[i][1]))
                
                hit_middle = 0

            for b in button_num:
                flag, num = b.button_clicked()
                if flag:
                    num_clicked = num
                
            for b in button_amount:
                flag, amount = b.button_clicked()    
                if flag:
                    amount_clicked = amount            

        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    
    
      