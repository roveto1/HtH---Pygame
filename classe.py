from settings import *
from codigoantigo import *
import pygame
import os


class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(imagem_pasta, "gatito_anda_1.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (largura /2 , altura/2)
        self.y_vel = 5
    
    def update(self):
        self.rect.x += 2
        self.rect.y += self.y_vel
        if self.rect.bottom > altura - 200:
            self.y_vel = -5
        if self.rect.bottom < 200:
            self.y_vel = 5
        if self.rect.left > largura:
            self.rect.right = 0