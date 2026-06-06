import pygame
import sys
import random


screen_width = 800
screen_height = 600
fps = 60

class Player():
    def __init__(self,x,y):
        self.speed = 5
        self.speed = 5
        self.width = 70
        self.height = 70
        self.scrap = []
        self.cash=0
        raw_player = pygame.image.load("Assets/Player.png").convert_alpha()
        self.base_image = pygame.transform.smoothscale(raw_player, (self.width, self.height))
        self.base_rect = pygame.image.load("Assets/Player.png").get_rect()
        self.base_rect.x = x
        self.base_rect.y = y
        grabber_width =40
       
        grabber_height =40
        raw_grabber = pygame.image.load("Assets/Grabber.png").convert_alpha()

        self.handle = pygame.transform.smoothscale(raw_grabber, (grabber_width, grabber_height))
        self.handle_rect = self.handle.get_rect()
        self.handle_rect = pygame.image.load("Assets/Grabber.png").get_rect()
        self.handle_rect.centerx = self.base_rect.centerx
        self.handle_rect.y = self.base_rect.y -30

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.base_rect.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.base_rect.x += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.base_rect.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.base_rect.y += self.speed
        
        if self.base_rect.x >screen_height+110:
            self.base_rect.x = screen_height+110
        if self.base_rect.x <0:
            self.base_rect.x = 0
        self.base_rect.y = max(self.height, min(screen_width - self.height, self.base_rect.y))

        self.handle_rect.centerx = self.base_rect.centerx
        self.handle_rect.centerx += 6
        self.handle_rect.y = self.base_rect.y -30
    def draw(self,screen):
        screen.blit(self.base_image, self.base_rect)
        screen.blit(self.handle, self.handle_rect)
        



class Scrap():
    def __init__(self,type,x,y,radius,modifiers):
        self.modifier_types = {"":1,"shiny":1.5,"dirty":.75,"cracked":.5,"dense":2}
        self.type = type
        self.x = x
        self.y = y
        self.radius = radius
        self.value_conversion ={"iron":50,"copper":1,"gold":100,"diamond":500}
        self.modifiers = modifiers
        self.value =0
        self.color = (50,50,50)
        if self.type == "diamond":
            raw_image = pygame.image.load("Assets/Diamond_scrap_normal.png").convert_alpha()
        elif self.type == "gold":
            raw_image = pygame.image.load("Assets/Gold scrap.png").convert_alpha()
        elif self.type == "iron":
            raw_image = pygame.image.load("Assets/Iron_scrap_normal.png").convert_alpha()
        else:
            raw_image = pygame.image.load("Assets/copper_scrap_normal.png").convert_alpha()
        diameter = self.radius * 2
        self.image = pygame.transform.scale(raw_image, (diameter, diameter))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_value(self):
        self.value += self.value_conversion[self.type.lower()]
        for i in self.modifiers:
            if i in self.modifier_types:
                self.value *= self.modifier_types[i]

    def update(self):
        self.rect.y += 2
        
    def draw(self,screen):
        screen.blit(self.image, self.rect)
            

        
    

class Game():
    def __init__(self):
        self.scrap = []
        pygame.init()

        pygame.display.set_caption("Deep Space Salvage")
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.player = Player(screen_width /2,screen_height /2)
        self.running = True
        self.clock = pygame.time.Clock()
        self.types_scrap = ["iron","copper","gold","diamond"]
        self.modifiers = ["shiny","dirty","cracked","dense"]
        self.spawn_rate=2000
        self.spawn_timer =0
        self.font = pygame.font.SysFont(None, 50)
        self.scrap_display = self.font.render(f"Your amount of scrap is {len(self.player.scrap)}",True,"blue") 
        self.cash_display = self.font.render(f"Your amount of cash is {self.player.cash}",True,"blue")
        self.break_up_time =0
    def run(self):
        while self.running:
            self.handle_events()
            self.create_scrap()
            self.update()
            self.draw()
            self.clock.tick(fps)
        
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    def create_scrap(self):
        self.break_up_time+=1
        if self.break_up_time % 17 == 0:
            modifier = []
            scrap_type = ""
            type_decider = random.randint(1,1000)
            
            if type_decider >200 :
                # sets it to copper
                scrap_type = self.types_scrap[1]
            elif type_decider > 20:
                # sets it to iron
                scrap_type = self.types_scrap[0]
            elif type_decider >1:
                # sets it to gold

                scrap_type = self.types_scrap[2]
            else:
                # sets it to diamond

                scrap_type = self.types_scrap[3]


            type_decider = random.randint(1,100)
            if type_decider >40 and type_decider< 50:
                modifier.append("shiny")
            elif type_decider > 30:
                modifier.append("dirty")
            elif type_decider > 20:
                modifier.append("cracked")
            elif type_decider > 10:
                modifier.append("dense")
            else:
                modifier.append("")



            new_scrap = Scrap(scrap_type,random.randint(1,800),0,random.randint(10,30),modifier)
            self.scrap.append(new_scrap)
            self.break_up_time =0
        else:
            pass

    def update(self):
        self.player.handle_input()
        self.spawn_timer += 1  
        self.scrap_display = self.font.render(f"Your amount of scrap is {len(self.player.scrap)}",True,"blue")
        if self.spawn_timer >= self.spawn_rate:
            self.create_scrap()   
            self.spawn_timer = 0
        for i in self.scrap:
            i.update()

            if i.rect.y > screen_height-35:
                self.scrap.remove(i)

            if self.player.handle_rect.colliderect(i.rect):
                self.scrap.remove(i)
                self.player.scrap.append(i)
                
        
    def draw(self):
        self.screen.fill("red")
        for i in self.scrap:
            i.draw(self.screen)
        self.player.draw(self.screen)

        self.screen.blit(self.scrap_display,(5,20))
        self.screen.blit(self.cash_display,(5,55))
        
        pygame.display.flip()
mygame =Game()
mygame.run()
