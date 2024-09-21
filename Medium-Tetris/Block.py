import pygame

TILE_SIZE = 50
T

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.image.fill('orange')
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]


class Tetromino():
    def __init__(self)