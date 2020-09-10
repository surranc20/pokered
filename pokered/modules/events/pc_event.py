class PC_Event():
    def __init__(self, player):
        self.player = player
        self.is_dead = False

    def draw(self, draw_surface):
        pass

    def update(self, ticks):
        pass

    def handle_event(self, event):
        pass

    def is_over(self):
        return self.is_dead
