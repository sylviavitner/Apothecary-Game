class Background():
    def __init__(self):
        self.colors = [(60, 163, 112), (150, 66, 83)] # map, shop
        self.state = 0
        self.current_bg = self.colors[self.state]

    def set_state(self, state):
        self.state = state
        self.current_bg = self.colors[self.state]
