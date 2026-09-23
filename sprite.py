# this will handle sprite interactions, hiding/showing sprites, etc.

import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, img, size, num_frames, x_pos, y_pos, scale=5, frame=0):
        pygame.sprite.Sprite.__init__(self)
        self.images = pygame.image.load(img).convert_alpha()
        self.scale = scale
        self.size = size
        self.num_frames = num_frames
        self.frame = frame
        self.frames_list = self.get_frames()
        self.rect = self.frames_list[0].get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.image = self.frames_list[self.frame]
        self.show = True
       
    def get_image(self, frame, scale):
        img = pygame.Surface((self.size, self.size), pygame.SRCALPHA).convert_alpha()
        img.blit(self.images, (0, 0), (frame * self.size, 0, self.size, self.size))
        img = pygame.transform.scale(img, (self.size * scale, self.size * scale))
        return img
    
    def get_frames(self):
        frames = []
        for i in range(self.num_frames):
            frame = self.get_image(i, self.scale)
            frames.append(frame)
        return frames

    def set_frame(self, frame):
        if frame < self.num_frames:
            self.frame = frame
            self.image = self.frames_list[self.frame]

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def set_state(self, state):
        if state == 0:
            self.show = False
        else:
            self.show = True

    def draw(self, screen):
        if self.show:
            screen.blit(self.image, (self.rect.x, self.rect.y))