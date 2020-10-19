from .utils.UI.drawable import Drawable


class Types(Drawable):
    TYPE_LOOKUP = {"normal": (0, 0), "fight": (1, 0), "flying": (2, 0),
                   "poison": (0, 1), "ground": (1, 1), "rock": (2, 1),
                   "bug": (0, 2), "ghost": (1, 2), "steel": (2, 2),
                   "fire": (0, 3), "water": (1, 3), "grass": (2, 3),
                   "electric": (0, 4), "psychic": (1, 4), "ice": (2, 4),
                   "dragon": (0, 5), "dark": (1, 5), "???": (2, 5)}

    def __init__(self, type_name):
        _offset = self.TYPE_LOOKUP[type_name.lower()]
        super().__init__("types.png", (0, 0), offset=_offset)
