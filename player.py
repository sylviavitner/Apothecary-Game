# player class

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, img, screen):
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
        self.rect.center = screen.get_rect().center # center sprite instead
        self.frame = 0
        self.image = self.frames_list[self.frame]
        self.last_update = pygame.time.get_ticks()
        # to keep track of player movement relative to other objects.
        # other sprites on map move by -dx, -dy * player speed
        self.dx = 0
        self.dy = 0

        # Shop variables
        self.allow_shop_entry = False
        self.inside_shop = False
        self.shop_input_active = True # change to True when done debugging
        self.shop_name = ""
        self.max_name_length = 20

        # Material variables
        self.berry_count = 0

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

    def move(self, current_time): # eventually list of sprites instead of just shop
        keys = pygame.key.get_pressed()
        self.moving = False
        self.dx = 0
        self.dy = 0
        if not self.shop_input_active:
            # movement
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction = "right"
                self.dx += 1
                self.moving = True
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction = "left"
                self.dx -= 1
                self.moving = True
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.dy -= 1
                self.moving = True
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.dy += 1
                self.moving = True     

        self.update_frame(current_time)

    def check_collisions(self, m_sprites):
        for s in m_sprites:
            if self.inside_shop:
                s.set_state(0)
                return
            else:
                s.set_state(1)

            # allow shop entry when interacting with shop sprite
            if s.name == "shop":
                if pygame.sprite.collide_rect(self, s):
                    self.allow_shop_entry = True
                    s.set_frame(1)
                else:
                    self.allow_shop_entry = False
                    s.set_frame(0)

            # allow harvest when interacting with bush sprite
            if s.name == "bush":
                if pygame.sprite.collide_rect(self, s):
                    if s.has_berries:
                        s.set_frame(3)
                        s.can_harvest = True
                    #else:
                        #s.set_frame(1) *no more interaction frame when bush is berryless*
                else:
                    if s.has_berries:
                        s.set_frame(2)
                    else:
                        s.set_frame(0)

    # just adds a berry to the count (for now)
    def harvest_bush(self):
        self.berry_count += 1

    def handle_event(self, event, background, shop, m_sprites):
        # get shop name input
        if event.type != pygame.KEYDOWN:
            return
        if self.shop_input_active:
            if event.key == pygame.K_BACKSPACE:
                self.shop_name = self.shop_name[:-1]
            elif event.key == pygame.K_RETURN:
                if self.shop_name.strip():
                    self.shop_input_active = False
                    shop.shop_name = self.shop_name
            elif len(self.shop_name) < self.max_name_length and event.unicode.isprintable():
                self.shop_name += event.unicode

        # setting states for sprite interactions
        elif event.key == pygame.K_e:
            if not self.inside_shop and self.allow_shop_entry:
                self.inside_shop = True
                background.set_state(1) # changes color
                for s in m_sprites:
                    s.set_state(0) # hide all map sprites
            elif not self.inside_shop and not self.allow_shop_entry:
                for s in m_sprites:
                    if s.name == "bush" and s.can_harvest:
                        # harvesting berries
                        s.can_harvest = False
                        s.has_berries = False
                        s.set_frame(0)
                        self.harvest_bush()
            elif self.inside_shop:
                self.inside_shop = False
                background.set_state(0)
                shop.set_state(0)

    def get_shop_name(self):
        self.shop_input_active = True

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


