# player class

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)

        # player vars
        self.images = {
            "right": pygame.image.load(img).convert_alpha(),
            "left": pygame.transform.flip(pygame.image.load(img).convert_alpha(), True, False) # flip img for going left
        }
        self.num_frames = 4
        self.moving = False
        self.direction = "right"
        self.scale = 3
        self.speed = 5
        self.frames_list = self.get_frames()
        self.frame_cooldown = 250
        self.rect = self.frames_list[0].get_rect()
        self.rect.x = 400
        self.rect.y = 400
        self.frame = 0
        self.image = self.frames_list[self.frame]
        self.last_update = pygame.time.get_ticks()

        # Shop variables
        self.allow_shop_entry = False
        self.inside_shop = False
        self.shop_input_active = False # change to True when done debugging
        self.shop_name = ""
        self.max_name_length = 10

    # gets an img from sprite sheet
    def get_image(self, w, h, frame, scale):
        img = pygame.Surface((w, h), pygame.SRCALPHA).convert_alpha()
        img.blit(self.images[self.direction], (0, 0), (frame * w, 0, w, h))
        img = pygame.transform.scale(img, (w * scale, h * scale))
        return img

    def get_frames(self):
        frames = []
        for i in range(self.num_frames):
            self.direction = "right"
            frame = self.get_image(32, 32, i, self.scale)
            frames.append(frame)
        return frames

    def update_frame(self, current_time):
        if self.moving:
            if current_time - self.last_update >= self.frame_cooldown:
                self.last_update = current_time
                self.frame +=1
                if self.frame >= 4:
                    self.frame = 0
        else:
            self.frame = 0
        self.image = self.frames_list[self.frame]
        # update image to face left
        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)

    def move(self, current_time, background, shop): # eventually list of sprites instead of just shop
        keys = pygame.key.get_pressed()
        self.moving = False
        if not self.shop_input_active:
            # movement
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.rect.x += self.speed
                self.direction = "right"
                self.moving = True
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.rect.x -= self.speed
                self.direction = "left"
                self.moving = True
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.rect.y -= self.speed
                self.moving = True
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.rect.y += self.speed
                self.moving = True     

        self.update_frame(current_time)

    def check_collisions(self, shop):
        if self.inside_shop:
            return
        if pygame.sprite.collide_rect(self, shop):
            self.allow_shop_entry = True
            shop.set_state(1)
        else:
            self.allow_shop_entry = False
            shop.set_state(0)

    def handle_event(self, event, background, shop):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if not self.inside_shop and self.allow_shop_entry:
                self.inside_shop = True
                background.set_state(1) # changes color
                shop.set_state(2) # hide shop
            elif self.inside_shop:
                self.inside_shop = False
                background.set_state(0)
                shop.set_state(0)


    def get_shop_name(self):
        self.shop_input_active = True

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


