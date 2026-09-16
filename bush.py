import pygame

class Bush(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)

        self.images = pygame.image.load(img).convert_alpha()
        self.num_frames = 4
        self.scale = 5
        self.size = 32 # 32x32 pixels
        self.frames_list = self.get_frames()
        self.frame = 0
        # temporary pos
        self.rect = self.frames_list[0].get_rect()
        self.rect.x = 600
        self.rect.y = 400
        self.image = self.frames_list[self.frame]

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

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


