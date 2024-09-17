import pygame
import random
from pygame.locals import *
from Bird import Bird
from Pipe import Pipe

pygame.init()
clock = pygame.time.Clock()
fps = 60

SCREEN_WITHT = 864
SCREEN_HEIGHT = 736
GROUND_X_POS = 0
GROUND_Y_POS = 568
LOOP_SPEED = 4  
BIRD_X_POS = 100
BIRD_Y_POS = int (SCREEN_HEIGHT / 2) - 100
COORDINATE_RESET_GROUND = 35

FLYING = False
GAME_OVER = False

TIME_FREQUENCY = 1500
LAST_PIPE = pygame.time.get_ticks()

font  = pygame.font.SysFont('Bauhaus 93', 60)

def draw_text(text, font, color, x , y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

score = 0
pass_pipe = False

screen = pygame.display.set_mode((SCREEN_WITHT, SCREEN_HEIGHT))
pygame.display.set_caption("Plappy Bird")

background = pygame.image.load('asset/bg.png')
ground = pygame.image.load('asset/ground.png')

bird_group = pygame.sprite.Group() 
flappy = Bird(BIRD_X_POS, BIRD_Y_POS)
bird_group.add(flappy)
pipe_group = pygame.sprite.Group()


run = True
while run: 
    clock.tick(fps)
    screen.blit(background, (0, 0))

    bird_group.draw(screen) 
    bird_group.update(FLYING, GAME_OVER) 
    pipe_group.draw(screen)
    pipe_group.update(LOOP_SPEED, GAME_OVER)

    screen.blit(ground, (GROUND_X_POS, GROUND_Y_POS))
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    draw_text(str(score), font, (255, 255, 255), int(SCREEN_WITHT / 2), 20)
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        GAME_OVER = True
    
    if flappy.rect.bottom > GROUND_Y_POS:
        GAME_OVER = True
        FLYING = False



    if GAME_OVER == False:
        if FLYING == True:
            current_time = pygame.time.get_ticks()
            if current_time - LAST_PIPE > TIME_FREQUENCY:
                pipe_height = random.randint(-100, 100)
                btm_Pipe = Pipe(SCREEN_WITHT, int (SCREEN_HEIGHT / 2) + pipe_height, -1)
                top_Pipe = Pipe(SCREEN_WITHT, int (SCREEN_HEIGHT / 2) + pipe_height, 1)
                pipe_group.add(btm_Pipe)
                pipe_group.add(top_Pipe)
                LAST_PIPE = current_time

        GROUND_X_POS -= LOOP_SPEED
        if abs(GROUND_X_POS) > COORDINATE_RESET_GROUND:
            GROUND_X_POS = 0    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and FLYING == False:
            FLYING = True
                
    pygame.display.update()

pygame.quit()