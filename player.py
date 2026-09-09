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
        self.speed = 3
        self.frames_list = self.get_frames()
        self.frame_cooldown = 250
        self.rect = self.frames_list[0].get_rect()
        self.rect.x = 400
        self.rect.y = 400
        self.frame = 0
        self.image = self.frames_list[self.frame]
        self.last_update = pygame.time.get_ticks()

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



    def move(self, current_time):
        keys = pygame.key.get_pressed()
        self.moving = False
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = "right"
            self.moving = True
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = "left"
            self.moving = True
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.moving = True
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.moving = True

        self.update_frame(current_time)


    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


