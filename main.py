import pygame
import sys
import random
import math

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
        raw_player = pygame.image.load("Assets/sprites/Player.png").convert_alpha()
        self.base_image = pygame.transform.smoothscale(raw_player, (self.width, self.height))
        self.base_rect = pygame.image.load("Assets/sprites/Player.png").get_rect()
        self.base_rect.x = x
        self.base_rect.y = y
        grabber_width =40
       
        grabber_height =40
        raw_grabber = pygame.image.load("Assets/sprites/Grabber.png").convert_alpha()

        self.handle = pygame.transform.smoothscale(raw_grabber, (grabber_width, grabber_height))
        self.handle_rect = self.handle.get_rect()
        self.handle_rect = pygame.image.load("Assets/sprites/Grabber.png").get_rect()
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
        
        if self.base_rect.x >screen_width-110:
            self.base_rect.x = screen_width -110
        if self.base_rect.x <0:
            self.base_rect.x = 0
        self.base_rect.y = max(self.height, min(screen_width - self.height, self.base_rect.y))

        self.handle_rect.centerx = self.base_rect.centerx
        self.handle_rect.centerx += 6
        self.handle_rect.y = self.base_rect.y -30
    def draw(self,screen):
        screen.blit(self.base_image, self.base_rect)
        screen.blit(self.handle, self.handle_rect)
        


class Drone():
    def __init__(self,x = screen_width//2+random.randint(-30,30),y=screen_height//2+random.randint(-30,30)):
        self.x = x
        self.y = y
        self.level = 1
        self.max_level = 5
        self.upgrade_stats = {
            1: {"speed": 2, "radius": 20, "modifier": 1.0},
            2: {"speed": 5, "radius": 40, "modifier": 1.0},
            3: {"speed": 5, "radius": 75, "modifier": 1.2},
            4: {"speed": 7, "radius": 90, "modifier": 1.5},
            5: {"speed": 10, "radius": 150, "modifier": 2.0}
        }
        self.update_stats()
        if self.level ==1:
            self.raw_drone = pygame.image.load("Assets/sprites/drone_upgrade1.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.raw_drone, (50, 50))
        self.rect = self.image.get_rect(center=(self.x, self.y))
    def update_stats(self):
            stats = self.upgrade_stats[self.level]
            self.speed = stats["speed"]
            self.pickup_radius = stats["radius"]
            self.value_modifier = stats["modifier"]
    def upgrade_level(self):
        if self.level <self.max_level:
            self.level+=1
            self.update_stats()
        else:
            pass
    def fly_to_target(self,scrap_list):
        if not scrap_list:
            return
        closest_scrap = None
        closest_dist = float("inf")
        for scrap in scrap_list:
            dx = self.rect.centerx - scrap.rect.centerx
            dy = self.rect.centerx - scrap.rect.centerx
            distance = math.sqrt((dx ** 2)+(dy ** 2))
            if distance < closest_dist:
                closest_dist = distance
                closest_scrap = scrap
        if closest_scrap:
            dx = closest_scrap.rect.centerx - self.rect.centerx
            dy = closest_scrap.rect.centery - self.rect.centery
            if closest_dist != 0:
                self.rect.x += (dx / closest_dist) * self.speed
                self.rect.y += (dy / closest_dist) * self.speed
    def check_pickup(self, scrap_list, player_inventory):
        for scrap in scrap_list[:]: 
            dx = scrap.rect.centerx - self.rect.centerx
            dy = scrap.rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)

   
            if distance <= self.pickup_radius:
                scrap_list.remove(scrap)
                
                scrap.value *= self.value_modifier 

                player_inventory.append(scrap)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
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
            raw_image = pygame.image.load("Assets/sprites/Diamond_scrap_normal.png").convert_alpha()
        elif self.type == "gold":
            raw_image = pygame.image.load("Assets/sprites/Gold scrap.png").convert_alpha()
        elif self.type == "iron":
            raw_image = pygame.image.load("Assets/sprites/Iron_scrap_normal.png").convert_alpha()
        else:
            raw_image = pygame.image.load("Assets/sprites/copper_scrap_normal.png").convert_alpha()
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
        return self.value
        

    def update(self):
        self.rect.y += 2
        
    def draw(self,screen):
        screen.blit(self.image, self.rect)
            

        
    

class Game():
    def __init__(self):
        self.scrap = []
        self.drones= []
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
        self.in_start = True
        
        
        self.background = pygame.image.load("Assets/sprites/Background.png").convert_alpha()

        self.hover_start =False
        
        self.in_menu = False


        self.start_button = pygame.image.load("Assets/sprites/start_button.png").convert_alpha()
        self.start_button = pygame.transform.scale(self.start_button,(300,225))
        self.start_button_main = self.start_button
        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.center = (screen_width // 2, screen_height // 3)

        
        self.sold_text_lines = []     
        self.sell_timer = 0           
        self.sell_timer_duration = 2 * fps

        self.start_button_hover = pygame.image.load("Assets/sprites/start_button_hover.png").convert_alpha()
        self.start_button_hover = pygame.transform.scale(self.start_button_hover,(300,225))


        

        self.menu_button =  pygame.image.load("Assets/sprites/menu_button.png").convert_alpha()
        self.menu_button = pygame.transform.scale(self.menu_button,(150,175))
        self.menu_button_main = self.menu_button
        self.menu_button_rect = self.menu_button.get_rect()
        self.menu_button_rect.center = (screen_width -100, screen_height -500)
        self.menu_button_hover = pygame.image.load("Assets/sprites/menu_button_hover.png")
        self.menu_button_hover= pygame.transform.scale(self.menu_button_hover,(150,100))

        
        self.sell_button = pygame.image.load("Assets/sprites/sell_button.png").convert_alpha()
        self.sell_button = pygame.transform.scale(self.sell_button,(150,100))
        self.sell_button_main = self.sell_button
        self.sell_button_rect = self.sell_button.get_rect()
        self.sell_button_rect.center = (screen_width -100, screen_height -300)
        self.sell_button_hover = pygame.image.load("Assets/sprites/sell_button_hover.png")
        self.sell_button_hover= pygame.transform.scale(self.sell_button_hover,(150,100))

        self.buy_drone_button = pygame.image.load("Assets/sprites/buy_drone_button.png").convert_alpha()
        self.buy_drone_button = pygame.transform.scale(self.buy_drone_button,(150,100))
        self.buy_drone_button_main = self.buy_drone_button
        self.buy_drone_button_rect = self.buy_drone_button.get_rect()
        self.buy_drone_button_rect.center = (screen_width -100, screen_height -200)
        self.buy_drone_button_hover = pygame.image.load("Assets/sprites/buy_drone_button_hover.png")
        self.buy_drone_button_hover= pygame.transform.scale(self.buy_drone_button_hover,(150,100))

        self.mouse_position =pygame.mouse.get_pos()
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
            self.mouse_position =pygame.mouse.get_pos()
            if self.start_button_rect.collidepoint(self.mouse_position):
                self.start_button_main = self.start_button_hover
            else:
                self.start_button_main = self.start_button
            if self.sell_button_rect.collidepoint(self.mouse_position):
                self.sell_button_main = self.sell_button_hover

            else:
                self.sell_button_main = self.sell_button
            if self.buy_drone_button_rect.collidepoint(self.mouse_position):
                self.buy_drone_button_main = self.buy_drone_button_hover

            else:
                self.buy_drone_button_main = self.buy_drone_button
            if self.menu_button_rect.collidepoint(self.mouse_position):
                self.menu_button_main = self.menu_button_hover

            else:
                self.menu_button_main = self.menu_button

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.start_button_rect.collidepoint(event.pos):
                        self.in_start = False
                    if self.in_start:
                        pass
                    else:
                        if self.menu_button_rect.collidepoint(event.pos):
                            self.in_menu = not self.in_menu
                        if self.in_menu:
                            if self.sell_button_rect.collidepoint(event.pos):
                                self.sell()
                            if self.buy_drone_button_rect.collidepoint(event.pos):
                                self.buy_drone()
                            
    def buy_drone(self):
        drone = Drone()
        self.drones.append(drone)

    def create_scrap(self):
        if self.in_start == True:
            pass
        else:
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



                new_scrap = Scrap(scrap_type,random.randint(75,screen_width-75),0,random.randint(10,30),modifier)
                self.scrap.append(new_scrap)
                self.break_up_time =0
            else:
                pass
    def sell(self):
        if not self.player.scrap:
            return  

        amounts = {}
        total_cash_gained = 0
        
       
        for item in self.player.scrap:
            value_gained = item.get_value()
            self.player.cash += value_gained
            total_cash_gained += value_gained
            
            
            mod_str = item.modifiers[0] if item.modifiers and item.modifiers[0] != "" else ""
            item_type = item.type
            
            
            key = (mod_str, item_type)
            amounts[key] = amounts.get(key, 0) + 1

        
        self.sold_text_lines = []
        
      
        for (modifier, item_type), amount in amounts.items():
            
            mod_display = f"{modifier} " if modifier else ""
            

            type_display = f"{item_type}s" if amount > 1 else item_type
            

            text_string = f"You sold {amount} {mod_display} {type_display}"
            self.sold_text_lines.append(text_string)
            

        self.sold_text_lines.append(f"Total Gained: +${total_cash_gained}")


        self.player.scrap.clear()
        self.cash_display = self.font.render(f"Your amount of cash is {self.player.cash}", True, "blue")
        self.sell_timer = self.sell_timer_duration 

    def update(self):
        if self.in_start == True:
            return
        if self.sell_timer > 0:
            self.sell_timer -= 1
        else:
            if self.in_menu:
                pass
            else:
                self.player.handle_input()
                self.spawn_timer += 1  
                self.scrap_display = self.font.render(f"Your amount of scrap is {len(self.player.scrap)}",True,"blue")
                if self.spawn_timer >= self.spawn_rate:
                    self.create_scrap()   
                    self.spawn_timer = 0
                for scrap in self.scrap[:]:
                    scrap.update()

                    if scrap.rect.y > screen_height-35:
                        self.scrap.remove(scrap)

                    if self.player.handle_rect.colliderect(scrap.rect):
                        self.scrap.remove(scrap)
                        self.player.scrap.append(scrap)
                for drone in self.drones:
                    drone.fly_to_target(self.scrap)
                    drone.check_pickup(self.scrap,self.player.scrap)
                    
        
    def draw(self):
        self.screen.blit(self.background,(0,0))

        if self.in_start == True:

                self.screen.blit(self.start_button_main,self.start_button_rect)
        else:
            self.screen.blit(self.menu_button_main,self.menu_button_rect)
            self.screen.blit(self.scrap_display,(5,20))
            self.screen.blit(self.cash_display,(5,55))
            if self.in_menu:

                self.screen.blit(self.sell_button_main,self.sell_button_rect)
                self.screen.blit(self.buy_drone_button_main,self.buy_drone_button_rect)

                
            else:
                for scrap in self.scrap:
                    scrap.draw(self.screen)
                for drone in self.drones:
                    drone.draw(self.screen)

                self.player.draw(self.screen)
                

            
        if self.sell_timer > 0:
            start_y = 150  
            for text_line in self.sold_text_lines:
                text_surface = self.font.render(text_line, True, "blue")
                text_rect = text_surface.get_rect(center=(screen_width // 2, start_y))
                self.screen.blit(text_surface, text_rect)
                start_y += 40
        pygame.display.flip()
mygame =Game()
mygame.run()
