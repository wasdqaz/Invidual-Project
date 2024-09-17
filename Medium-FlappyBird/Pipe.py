import pygame

PIPE_GAP = 150


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('asset/pipe.png')
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - PIPE_GAP/2]
        else:
            self.rect.topleft = [x, y + PIPE_GAP/2]  
    def update(self, scroll_speed, isGameOver):
        if isGameOver == False:
            self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
    def reset(self, x):
        self.rect.x = x