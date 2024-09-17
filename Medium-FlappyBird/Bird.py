import pygame

BIRD_FRAMES = 3
ANIMATION_LIMIT = 5 #Handle animation speed
VELOCITY = 0.5

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.animation_speed = 0
        for num in range(BIRD_FRAMES):
            img = pygame.image.load(f'asset/bird{num + 1}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity = 0
        self.clicked = False

    def update(self, isFly, isGameOver):
        #gravity
        if isFly:
            self.velocity += VELOCITY
            if self.velocity > 8: 
                self.velocity = 8
            if self.rect.bottom < 568 :
                self.rect.y += int(self.velocity)

        #jump
        if isGameOver == False:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and self.clicked == False:
                self.velocity = -9
                self.clicked = True
            if keys[pygame.K_SPACE] == 0:
                self.clicked = False

            #handle bird animation
            self.animation_speed += 1
            if self.animation_speed > ANIMATION_LIMIT:
                self.index = (self.index + 1) % BIRD_FRAMES
                self.animation_speed = 0
            self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -3)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)