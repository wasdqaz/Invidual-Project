from Setting import *
from Engine import Game, Score, Preview


class App():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        #Initial setting
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.screen.fill(GRAY)

        #components
        self.game = Game(self.screen)
        self.score = Score(self.screen)
        self.preview = Preview(self.screen)

        

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            #components
            self.game.run()
            self.score.run()
            self.preview.run()

            pygame.display.update()
            self.clock.tick()
if __name__ == '__main__':      
    app = App()
    app.run()