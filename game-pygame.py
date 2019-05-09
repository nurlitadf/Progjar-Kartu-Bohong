import pygame
from pygame.locals import *


pygame.init()
screen = pygame.display.set_mode((960, 540))

background = pygame.image.load("assets/bg.jpg")

while(True):
    screen.fill(0)

    #draw the background
    screen.blit(background, (0, 0))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)