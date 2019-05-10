import pygame
pygame.init()

class Button(object):
    def __init__(self, path, x, y):
        self.image = pygame.image.load(path).convert_alpha()
        self.path = path
        self.name = path.split('/')[1].split('.')[0]
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.status = 0

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def button_clicked(self, buttons):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            for button in buttons:
                button.status = 0
            self.status = 1