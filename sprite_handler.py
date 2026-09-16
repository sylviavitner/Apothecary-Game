# this will handle sprite interactions, hiding/showing sprites, etc.

import pygame

class SpriteHandler():
    def __init__(self):
        self.sprite_dict = {}

    def set_sprite_dict(self, sprites):
        pass

    # will need to move sprites when the player is touching a boundary and moving
    # look at pygame cameras
    def move_sprites(self):
        for sprite in self.sprite_dict:
            pass
