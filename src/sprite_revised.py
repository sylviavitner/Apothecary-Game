# cleaned up sprite class that allows for ALL sprites to inherit from sprite class

import pygame

class SpriteRevised(pygame.sprite.Sprite):
    def __init__(self, img, size=32, num_frames=2, num_rows=1):
        pygame.sprite.Sprite.__init__(self)

        # all sprites have these
        self.images = pygame.image.load(img).convert_alpha # player and customer will overwrite
        self.name = None # set in children
        self.size = size
        self.num_frames = num_frames
        self.num_rows = num_rows
        self.frame = 0 # may be reset in children (buttons?)
        self.frames_list = self.get_frames()
        self.rect = self.frames_list[0].get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.show = True

        def get_image(self, frame, scale):
            img = pygame.Surface((self.size, self.size), pygame.SRCALPHA).convert_alpha()
            img.blit(self.images[self.direction], (0, 0), (frame * self.size, self.col_idx * self.size, self.size, self.size))
            img = pygame.transform.scale(img, (self.size * scale, self.size * scale))
            return img

        def get_frames(self):
            frames = []
            for i in range(self.num_frames):
                frame = self.get_image(self.size, self.size, i, self.scale)
                frames.append(frame)
            return frames

        def set_frame(self, frame):
            if frame < self.num_frames:
                self.frame = frame
                self.image = self.frames_list[self.frame]

        def set_state(self, state):
            if state == 0:
                self.show = False
            else:
                self.show = True

        def move(self, dx, dy):
            self.rect.x += dx
            self.rect.y += dy

        def draw(self, screen):
            if self.show:
                screen.blit(self.image, (self.rect.x, self.rect.y))


