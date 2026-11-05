import pygame
from random import randint

class Customer(pygame.sprite.Sprite):
    def __init__(self, img, screen, col_idx=0):
        pygame.sprite.Sprite.__init__(self)

        self.images = {
            "right": pygame.image.load(img).convert_alpha(),
            "left": pygame.transform.flip(pygame.image.load(img).convert_alpha(), True, False) # flip img for going left
        }
        self.size = 32
        self.num_frames = 4
        self.scale = 3
        self.speed = 5
        self.direction = "right"
        self.col_idx = col_idx # 0, 1, 2, 3 specifies column number for getting frames
        self.frames_list = self.get_frames()
        self.frame_cooldown = 250
        self.frame = 0
        self.rect = self.frames_list[0].get_rect()
        self.rect.center = screen.get_rect().midtop - (self.size * self.scale)
        self.start_x = self.rect.x
        self.start_y = self.rect.y
        self.image = self.frames_list[self.frame]
        self.last_update = pygame.time.get_ticks()
        self.show = False
        self.moving = True
        self.desired_stand = None
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
                self.image = pygame.transform.slip(self.image, True, False)

    # choose to buy an item (or not)
    def choose_an_item(self, stand_list):
        i = randint(0, len(stand_list))
        stand = stand_list[i]
        buy_chance = 0 # out of 100

        # price per unit and market price determine odds of a successful purchase
        if stand.price_per_unit <= stand.market_price * 0.5:
            buy_chance = 99
        elif stand.price_per_unit <= stand.market_price * 0.8:
            buy_chance = 80
        elif stand.price_per_unit > stand.market_price * 0.8 <= stand.market_price * 1.2:
            buy_chance = 70
        elif stand.price_per_unit > stand.market_price * 1.2 <= stand.market_price * 1.6:
            buy_chance = 33
        elif stand.price_per_unit > stand.market_price * 1.6 <= stand.market_price * 2:
            buy_chance = 10
        else: # greater than 2x market
            buy_chance = 0

        x = randint(1, 100) # decide to buy or not

        if buy_chance <= x:
            self.desired_stand = stand
            self.desired_quantity = randint(1, stand.quantity) # choose random quantity

    def buy_item(self):
        print("Item bought") #todo
 
    def handle_movement(self, player, target_stand, current_time):
        
        target_x, target_y = target_stand.rect.x, target_stand.rect.y
       
        if player.inside_shop: # need another variable (maybe in player) to see if shop is open
            if target_x < self.rect.x:
                self.direction = "left"
            else:
                self.direction = "right"

            # move to target and stop when there
            if self.state == 1:
                if self.rect.y < target_y:
                    self.rect.y += 1 * self.speed
                elif self.rect.x < target_x - self.size:
                    self.rect.x += 1 * self.speed
                elif self.rect.x > target_x - self.size:
                    self.rect.x -= 1 * self.speed

            # change state upon arriving at stand
            if self.state == 1 and self.rect.x == target_x and self.rect.y == target_y:
                self.state = 0
                self.arrival_time = current_time

            # change direction and state after the cooldown
            elif self.state == 0 and current_time - self.arrival_time >= self.buy_cooldown:
                if self.desired_stand:
                    self.buy_item()
                self.direction = "left" if self.direction == "right" else self.direction = "right"
                self.state = 2

            # exit shop
            elif self.state == 2:
                if self.rect.x < self.start_x:
                    self.rect.x += 1 * self.speed
                elif self.rect.x > self.start_x:
                    self.rect.x -= 1 * self.speed
                elif self.rect.y > self.start_y:
                    self.rect.y -= 1 * self.speed

    # visit the shop and (potentially) buy something
    def visit_shop(self, player, shop_sprites):
        if shop_sprites and player.inside_shop:
            active_listings = []
            for s in shop_sprites:
                if s.name == "item_stand" and not s.prompt_active:
                    if s.item:
                        active_listings.append(s)
            if active_listings:
                self.choose_an_item(active_listings)
            self.show



            

        
        

        