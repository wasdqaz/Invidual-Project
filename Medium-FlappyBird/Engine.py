import pygame
import random
from pygame.locals import *
from Bird import Bird
from Pipe import Pipe


class Engine:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = 60

        # Screen settings
        self.SCREEN_WIDTH = 864
        self.SCREEN_HEIGHT = 736
        self.GROUND_X_POS = 0
        self.GROUND_Y_POS = 568
        self.LOOP_SPEED = 4  
        self.COORDINATE_RESET_GROUND = 35

        # Game state variables
        self.FLYING = False
        self.GAME_OVER = False
        self.score = 0
        self.TIME_FREQUENCY = 1500
        self.pass_pipe = False
        self.LAST_PIPE = pygame.time.get_ticks()

        # Set up display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Plappy Bird")

        # Load assets
        self.background = pygame.image.load('asset/bg.png')
        self.ground = pygame.image.load('asset/ground.png')
        self.button = pygame.image.load('asset/restart.png')

        #create button
        self.button_rect = self.button.get_rect()
        self.button_X_POS = self.SCREEN_WIDTH / 2 - self.button_rect.width / 2
        self.button_Y_POS = self.SCREEN_HEIGHT / 2 - self.button_rect.height / 2
        self.button_rect.topleft = (self.button_X_POS, self.button_Y_POS)

        # Font
        self.font = pygame.font.SysFont('Bauhaus 93', 60)

        # Bird and pipe groups
        self.bird_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()

        # Create bird
        self.flappy = Bird(100, int(self.SCREEN_HEIGHT / 2) - 100)
        self.bird_group.add(self.flappy)

    def reset(self):
        self.GAME_OVER = False
        self.FLYING = False
        self.score = 0
        self.pass_pipe = False
        self.LAST_PIPE = pygame.time.get_ticks()
        self.flappy.reset(100, int(self.SCREEN_HEIGHT / 2) - 100)
        self.pipe_group.empty()

    def draw_button(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        self.screen.blit(self.button, self.button_rect)
        return action
    def draw_text(self, text, color, x, y):
        img = self.font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def reset_ground_position(self):
        self.GROUND_X_POS -= self.LOOP_SPEED
        if abs(self.GROUND_X_POS) > self.COORDINATE_RESET_GROUND:
            self.GROUND_X_POS = 0

    def generate_pipes(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.LAST_PIPE > self.TIME_FREQUENCY:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(self.SCREEN_WIDTH, int(self.SCREEN_HEIGHT / 2) + pipe_height, -1)
            top_pipe = Pipe(self.SCREEN_WIDTH, int(self.SCREEN_HEIGHT / 2) + pipe_height, 1)
            self.pipe_group.add(btm_pipe)
            self.pipe_group.add(top_pipe)
            self.LAST_PIPE = current_time

    def check_collision(self):
        if pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False) or self.flappy.rect.top < 0:
            self.GAME_OVER = True

        if self.flappy.rect.bottom > self.GROUND_Y_POS:
            self.GAME_OVER = True
            self.FLYING = False

    def update_score(self):
        if len(self.pipe_group) > 0:
            bird = self.bird_group.sprites()[0]
            first_pipe = self.pipe_group.sprites()[0]

            if bird.rect.left > first_pipe.rect.left and bird.rect.right < first_pipe.rect.right and not self.pass_pipe:
                self.pass_pipe = True
            if self.pass_pipe and bird.rect.left > first_pipe.rect.right:
                self.score += 1
                self.pass_pipe = False

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and not self.FLYING:
            self.FLYING = True
        return True

    def handle_gameover (self):
        if self.draw_button():
            self.reset()

    def run_game(self):
        running = True
        while running:
            self.clock.tick(self.fps)
            self.screen.blit(self.background, (0, 0))

            # Draw bird and pipes
            self.bird_group.draw(self.screen)
            self.bird_group.update(self.FLYING, self.GAME_OVER)
            self.pipe_group.draw(self.screen)
            self.pipe_group.update(self.LOOP_SPEED, self.GAME_OVER)
            
            # Draw ground
            self.screen.blit(self.ground, (self.GROUND_X_POS, self.GROUND_Y_POS))
            if self.GAME_OVER == False:
                self.reset_ground_position()

            # Update score
            self.update_score()
            self.draw_text(str(self.score), (255, 255, 255), int(self.SCREEN_WIDTH / 2), 20)

            # Check collisions
            self.check_collision()

            # Handle pipes
            if not self.GAME_OVER and self.FLYING:
                self.generate_pipes()

            # Handle input
            for event in pygame.event.get():
                running = self.handle_event(event)
            if self.GAME_OVER == True:
                self.handle_gameover()
            pygame.display.update()

        pygame.quit()

# if __name__ == "__main__":
#     engine = Engine()
#     engine.run_game()
