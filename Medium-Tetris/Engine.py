from Setting import *
from Block import Tetromino
import random

class Game:
    def __init__(self, window):

        #default setting
        self.game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        
        self.game_window = window
        self.rect = self.game_surface.get_rect(topleft = (PADDING, PADDING))
        
        self.timers = {
            'move down' : Timer(UPDATE_START_SPEED, True, self.move_down),
            'move horizontal' : Timer(MOVE_WAIT_TIME),
            'rotate' : Timer(ROTATE_WAIT_TIME)
        }

        self.data_field = [[0 for i in range(COLUMNS)] for j in range(ROWS)]



        self.timers['move down'].activate()
        self.sprites = pygame.sprite.Group()
        #test
        self.tetromino = Tetromino(
            self.sprites,
            random.choice(list(TETROMINOS.keys())),
           
            self.generate_tetromino,
            self.data_field)

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def handle_event(self):
        keys = pygame.key.get_pressed()
        if self.timers['move horizontal'].active == False:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['move horizontal'].activate()
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers['move horizontal'].activate()
        if not self.timers['rotate'].active:
            if keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers['rotate'].activate()
    def delete_rows(self):
        del_rows = []
        for i, row in enumerate(self.data_field):
            if all(row):
                del_rows.append(i)
        if del_rows:
            for del_row in del_rows:
                for block in self.data_field[del_row]:
                    block.kill()

                for row in self.data_field:
                    for block in row:
                        if block and block.pos.y < del_row:
                            block.pos.y+=1

        self.data_field = [[0 for i in range(COLUMNS)] for j in range(ROWS)]
        for block in self.sprites:
            self.data_field[int(block.pos.y)][int(block.pos.x)] = block
        
    def draw_grid(self):
        
        for col in range(1, COLUMNS):
            x_coor = col * CELL_SIZE
            pygame.draw.line(self.game_surface, LINE_COLOR, (x_coor, 0), (x_coor, self.game_surface.get_height()), 1)
        for row in range(1, ROWS):
            pygame.draw.line(self.game_surface, LINE_COLOR, (0, row * CELL_SIZE), (self.game_surface.get_width(), row * CELL_SIZE), 1)
    
    def move_down(self):
        self.tetromino.move_down()

    def generate_tetromino(self):
        self.delete_rows()
        self.tetromino = Tetromino(
            self.sprites,
            random.choice(list(TETROMINOS.keys())),
            self.generate_tetromino,
            self.data_field
        )

    def run(self):

        #handle user input (move left, right, increase speed )
        self.handle_event()

        #update
        self.timer_update()
        self.sprites.update()

        #draw
        self.game_surface.fill(GRAY)
        self.sprites.draw(self.game_surface)
        self.draw_grid()

        #window
        self.game_window.blit(self.game_surface, (PADDING, PADDING))
        pygame.draw.rect(self.game_window, LINE_COLOR, self.rect, 2, 2)

class Score:
    def __init__(self, window):
        self.score_surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING))
        self.score_window = window
    def run(self):
        self.score_window.blit(self.score_surface, (2 * PADDING + GAME_WIDTH, PADDING))

class Preview:
    def __init__(self, window):
        self.Preview_surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION))
        self.Preview_window = window
    def run(self):
        self.Preview_window.blit(self.Preview_surface, (2 * PADDING + GAME_WIDTH, PADDING + GAME_HEIGHT * SCORE_HEIGHT_FRACTION))

class Timer:
    def __init__(self, duration, repeated = False, Function = None):
        self.duration = duration
        self.repeated = repeated
        self.function = Function
        self.start_time = 0
        self.active = False
    
    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks() 
    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration and self.active:
            if self.function and self.start_time != 0:
                self.function()
            self.deactivate()

            if self.repeated:
                self.activate()