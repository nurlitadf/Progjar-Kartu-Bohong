import pygame
import os
pygame.init()


class Button(object):
    def __init__(self, path, x, y):
        self.image = pygame.image.load(path).convert_alpha()
        self.path = path
        self.name = os.path.basename(path).split('.')[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def button_clicked(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True


class ButtonNumber(Button):
    def __init__(self, path, x, y):
        super().__init__(path, x, y)

    def button_clicked(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True, self.name
        else:
            return False, "0"


class ButtonAmount(Button):
    def __init__(self, path, x, y):
        super().__init__(path, x, y)

    def button_clicked(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True, self.name
        else:
            return False, "0"
