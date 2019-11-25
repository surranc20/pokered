class Hit():
    def __init__(self, pokemon):
        self._pokemon = pokemon
        self._animation_timer = 0
        self._blink_num = 0
        self._fps = 9
        self._is_dead = False
    
    def draw(self, draw_surface):
        pass

    def is_dead(self):
        return self._is_dead
    
    def update(self, ticks):
        self._animation_timer += ticks
        if self._animation_timer > 1 / self._fps:
            self._animation_timer -= 1 / self._fps
            if self._blink_num < 8:
                self._blink_num += 1
                self._pokemon._draw = not self._pokemon._draw
            else:
                self._is_dead = True


