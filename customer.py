import pygame
from random import randint

class Customer(pygame.sprite.Sprite):
    def __init__(self, img, screen, col_idx=0):
        pygame.sprite.Sprite.__init__(self)

        self.images = {
            "right": pygame.image.load(img).convert_alpha(),
            "left": pygame.transform.flip(pygame.image.load(img).convert_alpha(), True, False) # flip img for going left
        }
        self.name = "customer"
        self.size = 32
        self.num_frames = 4
        self.scale = 3
        self.speed = 5
        self.direction = "right"
        self.col_idx = col_idx # 0, 1, 2, 3 specifies column number for getting frames
        self.frames_list = self.get_frames()
        self.frame_cooldown = 250
        self.frame = 0
        self.rect = self.frames_list[0].get_rect(midbottom=(screen.get_rect().centerx, -(self.size * self.scale)))
        self.start_x = self.rect.x
        self.start_y = self.rect.y
        self.image = self.frames_list[self.frame]
        self.last_update = pygame.time.get_ticks()
        self.arrival_time = pygame.time.get_ticks()
        self.show = False
        self.moving = True
        self.target_stand = None
        self.desired_quantity = 0
        self.state = 1 # 0, 1, 2 for still, entering, exiting
        self.buy_cooldown = 2000 # 2 secs until purchase

    def get_image(self, w, h, frame, scale):
        img = pygame.Surface((w, h), pygame.SRCALPHA).convert_alpha()
        img.blit(self.images[self.direction], (0, 0), (frame * w, self.col_idx * h, w, h))
        img = pygame.transform.scale(img, (w * scale, h * scale))
        return img

    def get_frames(self):
        frames = []
        for i in range(self.num_frames):
            self.direction = "right"
            frame = self.get_image(self.size, self.size, i, self.scale)
            frames.append(frame)
        return frames

    def update_frame(self, current_time):
        if self.moving:
            if current_time - self.last_update >= self.frame_cooldown:
                self.last_update = current_time
                self.frame += 1
                if self.frame >= self.num_frames:
                    self.frame = 0
        else:
            self.frame = 0

        self.image = self.frames_list[self.frame]

        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)

    # ONLY sets the state of alive or not, not enter, exit etc. state (not self.state)
    def set_state(self, state):
        if state == 0:
            self.kill() # just kill customers when they aren't on screen
        else:
            self.show = True

    # choose to buy an item (or not)
    def choose_an_item(self, stand_list):
        i = randint(0, len(stand_list) - 1)
        stand = stand_list[i]
        buy_chance = 0 # out of 100

        ppu = int(stand.price_per_unit)
        market = stand.market_price

        # price per unit and market price determine odds of a successful purchase
        if ppu <= market * 0.5:
            buy_chance = 99
        elif ppu <= market * 0.8:
            buy_chance = 80
        elif ppu > market * 0.8 <= market * 1.2:
            buy_chance = 70
        elif ppu > market * 1.2 <= market * 1.6:
            buy_chance = 33
        elif ppu > market * 1.6 <= market * 2:
            buy_chance = 10
        else: # greater than 2x market
            buy_chance = 0

        x = randint(1, 100) # decide to buy or not

        self.target_stand = stand

        if buy_chance <= x:
            self.desired_quantity = randint(1, stand.quantity) # choose random quantity
        else:
            self.desired_quantity = 0

    def move_toward_target_pos(self, target_x, target_y, current_time):
        if self.rect.y < target_y:
            self.rect.y += 1 * self.speed
            return
        elif target_x > self.start_x:
            if self.rect.x < target_x:
                self.direction = "right"
                self.rect.x += 1 * self.speed
                return
        elif target_x < self.start_x:
            if self.rect.x > target_x:
                self.direction = "left"
                self.rect.x -= 1 * self.speed
                return
            
        self.state = 0 # still
        self.moving = False
        self.arrival_time = current_time

    def exit_shop(self, target_x):
        if target_x > self.start_x:
            if self.rect.x > self.start_x:
                self.direction = "left"
                self.rect.x -= 1 * self.speed
                return
        elif target_x < self.start_x:
            if self.rect.x < self.start_x:
                self.direction = "right"
                self.rect.x += 1 * self.speed
                return
        if self.rect.y > self.start_y:
            self.rect.y -= 1 * self.speed
        else:
            self.kill() # delete when done
        
    
    def buy_item(self):
        print("Item bought") #todo
 
    def handle_movement(self, player, current_time):

        if not player.inside_shop or not player.shop_open or not self.show or not self.target_stand:
            self.set_state(0)
            return
        
        target_x, target_y = self.target_stand.rect.x, self.target_stand.rect.y

        # move to target and stop when there
        if self.state == 1:
            self.moving = True
            self.move_toward_target_pos(target_x, target_y, current_time)

        # change state after the cooldown
        elif self.state == 0:
            self.moving = False
            if current_time - self.arrival_time >= self.buy_cooldown:
                if self.target_stand:
                    self.buy_item()
                self.state = 2

        # exit shop
        elif self.state == 2:
            self.moving = True
            self.exit_shop(target_x)


    # visit the shop and (potentially) buy something
    def visit_shop(self, player, shop_sprites):
        if shop_sprites and player.inside_shop and player.shop_open:
            active_listings = []
            for s in shop_sprites:
                if s.name == "item_stand" and not s.prompt_active:
                    if s.item:
                        active_listings.append(s)
            if active_listings:
                self.choose_an_item(active_listings)
            self.show = True
        else:
            self.kill()
            return

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class CustomerHandler():
    def __init__(self):
        self.cooldown = 8000
        self.last_entered = pygame.time.get_ticks()

    def deploy_customer(self, player, current_time, screen, customers, shop_sprites):
        if not shop_sprites or not player.inside_shop or not player.shop_open:
            return
        elif current_time - self.last_entered >= self.cooldown:
            self.last_entered = current_time
            x = randint(0, 3) # number of customer frames
            customer = Customer("assets/customer.png", screen, x)
            customer.visit_shop(player, shop_sprites)
            customers.add(customer)
            shop_sprites.add(customer)




            

        
        

        