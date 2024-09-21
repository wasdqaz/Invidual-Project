import pygame
from pygame.locals import *
from Block import *


class GameEngine:
    def __init__(self):
        pygame.init()

        #DEFAULT SETTING
        TILE_SIZE = 50
        self.SCREEN_WIDTH = TILE_SIZE * 10
        self.SCREEN_HEIGHT = TILE_SIZE * 15
        self.run = True #app state

        #tetris block
        self.block_group = pygame.sprite.Group()
        
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Puzzle")

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        return True

    def generate_tetromino(self):
        tetro = Block(0,0)
        self.block_group.add(tetro)

    def draw(self):
        self.generate_tetromino()
        self.block_group.draw(self.screen)

    def draw_grid(self):
        for x in range(0, self.SCREEN_WIDTH, TILE_SIZE):
            for y in range(0, self.SCREEN_HEIGHT, TILE_SIZE):
                pygame.draw.rect(self.screen, 'white', (x, y, TILE_SIZE, TILE_SIZE), 1)

    def run_game(self):
        while self.run:
            self.screen.fill('black')  
            self.draw_grid()
            self.draw()
            pygame.display.flip()  
            for event in pygame.event.get():
                self.run = self.handle_event(event)

if __name__ == "__main__":
    engine = GameEngine()
    engine.run_game()
