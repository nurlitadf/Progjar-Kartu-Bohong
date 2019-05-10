import pygame
pygame.init()

class Card(object):
    def __init__(self, path, x, y):
        self.image = pygame.image.load(path).convert_alpha()
        self.path = path
        self.num = path.split('-')[0]
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.status = 0 #0 tidak aktif, 1 aktif (naik ke atas), 2 dipilih buat ditaruh di tengah

    def draw(self, screen):
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

class CardPlaced(Card):
    def __init__(self, path, x, y):
        self.image = pygame.image.load("assets/x.png").convert_alpha()
        self.path = path
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.status = 2
    
    
    
