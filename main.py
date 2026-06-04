import pygame
import sys
class Game():
    def __init__():
        screen_width = 800
        screen_height = 600
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    def update(self):
        pass
    def draw(self):
        pass
