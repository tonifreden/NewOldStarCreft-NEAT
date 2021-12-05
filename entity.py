import pygame
import random
import os

from pygame.locals import RLEACCEL
    

class BGEntity(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super(BGEntity, self).__init__()
        images = ["meteor", "planet", "asteroid", "saturn", "uranus"]
        self.image = images[random.randint(0, len(images) - 1)]
        self.surf = pygame.image.load(os.path.join("images", self.image + ".png")).convert()
        
        self.surf.set_colorkey((255, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(width + 20, width + 100),
                random.randint(0, height),
            )
        )
        
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()