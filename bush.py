from sprite import Sprite

class Bush(Sprite):
    def __init__(self, img, x_pos=600, y_pos=400):
        # now inherits from Sprite class
        super().__init__(img, size=32, num_frames=4, x_pos=x_pos, y_pos=y_pos, scale=5)


