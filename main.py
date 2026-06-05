import pygame
import sys
screen_width = 800
screen_height = 600
fps = 60
class Player():
    def __init__(self,x,y):
        self.speed = 5
        self.x = x
        self.y = y
        self.speed = 5
        self.width = 25
        self.height = 35
        self.scrap = []
        self.cash=0
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        self.x = max(self.width, min(screen_height - self.width, self.x))
        self.y = max(self.height, min(screen_width - self.height, self.y))
    def draw(self,screen):
        pygame.draw.rect(screen,"white", pygame.Rect( self.x, self.y,self.width, self.height))
class Scrap():
    def init(self,type,x,y,radius,size,modifiers):
        self.modifier_types = {"shiny":1.5,"dirty":.75,"cracked":.5,"dense":2}
        self.type = type
        self.x = x
        self.y = y
        self.radius = radius
        self.value_conversion ={"iron":50,"copper":1,"gold":100,"diamond":500}
        self.modifiers = modifiers
        self.value =0
    def get_value(self):
        self.value += self.value_conversion[self.type.lower()]
        for i in self.modifiers:
            if i in self.modifier_types:
                self.value += self.modifier_types[i]
    def update(self):
        self.x -= 1
    def draw(self,screen):
        pygame.draw.circle(screen,(50,50,50)(int(self.x), int(self.y)), self.radius)
    
            

        
    

class Game():
    def __init__(self):
        self.scrap = []
        pygame.init()

        pygame.display.set_caption("Deep Space Salvage")
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.player = Player(screen_width /2,screen_height /2)
        self.running = True
        self.clock = pygame.time.Clock()
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(fps)
        
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    def create_scrap():
    def update(self):
        self.player.handle_input()
    def draw(self):
        self.screen.fill((0,0,0))
        self.player.draw(self.screen)
        
        pygame.display.flip()
mygame =Game()
mygame.run()
