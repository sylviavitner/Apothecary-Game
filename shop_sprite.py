import pygame

class ShopSprite(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)

        self.images = pygame.image.load(img).convert_alpha()
        self.frames = []
        self.num_frames = 2
        self.scale = 5
        self.state = 0 # 0 = no collsion, 1 = player collision
        self.frames_list = self.get_frames()
        self.rect = self.frames_list[0].get_rect()
        self.rect.x = 800
        self.rect.y = 100
        self.frame = 0
        self.image = self.frames_list[self.frame]

    # stolen from player.py, just gets the img from the sprite sheet same as before
    def get_image(self, w, h, frame, scale):
        img = pygame.Surface((w, h), pygame.SRCALPHA).convert_alpha()
        img.blit(self.images, (0, 0), (frame * w, 0, w, h))
        img = pygame.transform.scale(img, (w * scale, h * scale))
        return img

    # gets the 2 frames from shop (no collision v sprite collison with player)
    def get_frames(self):
        frames = []
        for i in range(self.num_frames):
            frame = self.get_image(64, 64, i, self.scale) # 64 x 64 pixel imgs
            frames.append(frame)
        return frames

    # for now collisions are checked in main and this is called when player rect touches shop rect
    def set_state(self, state):
        self.frame = state
        self.image = self.frames_list[self.frame]

    def move(self):
        pass # will need to move opposite of player when the player reaches boundary of screen

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))




