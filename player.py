import pygame
import os
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super(Player, self).__init__()
        self.surf = pygame.image.load(os.path.join("images", "ufo.png")).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.width, self.height = ((width, height))
        self.speed = 10
        self.points = 0
        
    def move(self, direction: str):
        if direction == "up":
            self.rect.move_ip(0, -self.speed)
        if direction == "down":
            self.rect.move_ip(0, self.speed)
            
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.width:
            self.rect.right = self.width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.height:
            self.rect.bottom = self.height