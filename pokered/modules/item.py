import json
from os.path import join
from .enumerated.item_types import ItemTypes


class Item():
    ITEM_TYPES_DICT = {
        "potion": ItemTypes.ITEMS,
        "super potion": ItemTypes.ITEMS,
        "hyper potion": ItemTypes.ITEMS,
        "max potion": ItemTypes.ITEMS,
        "full restore": ItemTypes.ITEMS,
        "fresh water": ItemTypes.ITEMS,
        "soda pop": ItemTypes.ITEMS,
        "lemonade": ItemTypes.ITEMS,
        "moo moo milk": ItemTypes.ITEMS,
        "energy root": ItemTypes.ITEMS,
        "energy powder": ItemTypes.ITEMS,
        "berry juice": ItemTypes.ITEMS,
        "sacred ash": ItemTypes.ITEMS,
        "ether": ItemTypes.ITEMS,
        "max ether": ItemTypes.ITEMS,
        "elixer": ItemTypes.ITEMS,
        "max elixer": ItemTypes.ITEMS,
        "revival herb": ItemTypes.ITEMS,
        "revive": ItemTypes.ITEMS,
        "max revive": ItemTypes.ITEMS,
        "antidote": ItemTypes.ITEMS,
        "awakening": ItemTypes.ITEMS,
        "burn heal": ItemTypes.ITEMS,
        "ice heal": ItemTypes.ITEMS,
        "paralyz heal": ItemTypes.ITEMS,
        "full heal": ItemTypes.ITEMS,
        "lava cookie": ItemTypes.ITEMS,
        "heal powder": ItemTypes.ITEMS,
        'calcium': ItemTypes.ITEMS,
        "carbos": ItemTypes.ITEMS,
        "hp up": ItemTypes.ITEMS,
        "iron": ItemTypes.ITEMS,
        "pp max": ItemTypes.ITEMS,
        "pp up": ItemTypes.ITEMS,
        "protien": ItemTypes.ITEMS,
        "rare candy": ItemTypes.ITEMS,
        "zinc": ItemTypes.ITEMS,
        "dire hit": ItemTypes.ITEMS,
        "guard spec": ItemTypes.ITEMS,
        "x accuracy": ItemTypes.ITEMS,
        "x attack": ItemTypes.ITEMS,
        "x defend": ItemTypes.ITEMS,
        "x special": ItemTypes.ITEMS,
        "x speed": ItemTypes.ITEMS,
        "amulet coin": ItemTypes.ITEMS,
        "black belt": ItemTypes.ITEMS,
        "black glasses": ItemTypes.ITEMS,
        "bright powder": ItemTypes.ITEMS,
        "charcoal": ItemTypes.ITEMS,
        "choice band": ItemTypes.ITEMS,
        "cleanse tag": ItemTypes.ITEMS,
        "deep sea scale": ItemTypes.ITEMS,
        "deep sea tooth": ItemTypes.ITEMS,
        "dragon fang": ItemTypes.ITEMS,
        "dragon scale": ItemTypes.ITEMS,
        "everstone": ItemTypes.ITEMS,
        "exp share": ItemTypes.ITEMS,
        "focus band": ItemTypes.ITEMS,
        "hard stone": ItemTypes.ITEMS,
        "king's rock": ItemTypes.ITEMS,
        "lax incense": ItemTypes.ITEMS,
        "leftovers": ItemTypes.ITEMS,
        "light ball": ItemTypes.ITEMS,
        "lucky egg": ItemTypes.ITEMS,
        "lucky punch": ItemTypes.ITEMS,
        "macho brace": ItemTypes.ITEMS,
        "magnet": ItemTypes.ITEMS,
        "mental herb": ItemTypes.ITEMS,
        "metal coat": ItemTypes.ITEMS,
        "metal powder": ItemTypes.ITEMS,
        "miracle seed": ItemTypes.ITEMS,
        "mystic water": ItemTypes.ITEMS,
        "nevermeltice": ItemTypes.ITEMS,
        "poison barb": ItemTypes.ITEMS,
        "quick claw": ItemTypes.ITEMS,
        "scope lense": ItemTypes.ITEMS,
        "sea incense": ItemTypes.ITEMS,
        "shap beak": ItemTypes.ITEMS,
        "shell bell": ItemTypes.ITEMS,
        "silk scarf": ItemTypes.ITEMS,
        "silver powder": ItemTypes.ITEMS,
        "smoke ball": ItemTypes.ITEMS,
        "soft sand": ItemTypes.ITEMS,
        "soothe bell": ItemTypes.ITEMS,
        "soul dew": ItemTypes.ITEMS,
        "spell tag": ItemTypes.ITEMS,
        "stick": ItemTypes.ITEMS,
        "thick club": ItemTypes.ITEMS,
        "twisted spoon": ItemTypes.ITEMS,
        "white herb": ItemTypes.ITEMS,
        "blue scarf": ItemTypes.ITEMS,
        "green scarf": ItemTypes.ITEMS,
        "pink scarf": ItemTypes.ITEMS,
        "red scarf": ItemTypes.ITEMS,
        "yellow scarf": ItemTypes.ITEMS,
        "black flute": ItemTypes.ITEMS,
        "blue flute": ItemTypes.ITEMS,
        "red flute": ItemTypes.ITEMS,
        "white flute": ItemTypes.ITEMS,
        "yellow flute": ItemTypes.ITEMS,
        "moon stone": ItemTypes.ITEMS,
        "fire stone": ItemTypes.ITEMS,
        "leaf stone": ItemTypes.ITEMS,
        "thunderstone": ItemTypes.ITEMS,
        "sun stone": ItemTypes.ITEMS,
        "water stone": ItemTypes.ITEMS,
        "upgrade": ItemTypes.ITEMS,
        "blue shard": ItemTypes.ITEMS,
        "green shard": ItemTypes.ITEMS,
        "red shard": ItemTypes.ITEMS,
        "yellow shard": ItemTypes.ITEMS,
        "escape rope": ItemTypes.ITEMS,
        "fluffy tail": ItemTypes.ITEMS,
        "pokedoll": ItemTypes.ITEMS,
        "shoal salt": ItemTypes.ITEMS,
        "shoal shell": ItemTypes.ITEMS,
        "max repel": ItemTypes.ITEMS,
        "repel": ItemTypes.ITEMS,
        "super repel": ItemTypes.ITEMS,
        "big pearl": ItemTypes.ITEMS,
        "big mushroom": ItemTypes.ITEMS,
        "heart scale": ItemTypes.ITEMS,
        "nugget": ItemTypes.ITEMS,
        "pearl": ItemTypes.ITEMS,
        "star piece": ItemTypes.ITEMS,
        "stardust": ItemTypes.ITEMS,
        "tinymushroom": ItemTypes.ITEMS,
        "pokeball": ItemTypes.POKE_BALLS,
        "great ball": ItemTypes.POKE_BALLS,
        "ultra ball": ItemTypes.POKE_BALLS,
        "master ball": ItemTypes.POKE_BALLS,
        "dive ball": ItemTypes.POKE_BALLS,
        "luxury ball": ItemTypes.POKE_BALLS,
        "nest ball": ItemTypes.POKE_BALLS,
        "net ball": ItemTypes.POKE_BALLS,
        "premier ball": ItemTypes.POKE_BALLS,
        "repeat ball": ItemTypes.POKE_BALLS,
        "safari ball": ItemTypes.POKE_BALLS,
        "timer ball": ItemTypes.POKE_BALLS,
        "bead mail": ItemTypes.ITEMS,
        "dream mail": ItemTypes.ITEMS,
        "glitter mail": ItemTypes.ITEMS,
        "gorgeous mail": ItemTypes.ITEMS,
        "harbor mail": ItemTypes.ITEMS,
        "mech mail": ItemTypes.ITEMS,
        "orange mail": ItemTypes.ITEMS,
        "retro mail": ItemTypes.ITEMS,
        "shadow mail": ItemTypes.ITEMS,
        "tropic mail": ItemTypes.ITEMS,
        "wave mail": ItemTypes.ITEMS,
        "wood mail": ItemTypes.ITEMS,
        "aurora ticket": ItemTypes.KEY_ITEMS,
        "berry bag": ItemTypes.KEY_ITEMS,
        "bike": ItemTypes.KEY_ITEMS,
        "bike voucher": ItemTypes.KEY_ITEMS,
        "card key": ItemTypes.KEY_ITEMS,
        "coin case": ItemTypes.KEY_ITEMS,
        "dome fossil": ItemTypes.KEY_ITEMS,
        "fame checker": ItemTypes.KEY_ITEMS,
        "gold teeth": ItemTypes.KEY_ITEMS,
        "good rod": ItemTypes.KEY_ITEMS,
        "helix fossil": ItemTypes.KEY_ITEMS,
        "item finder": ItemTypes.KEY_ITEMS,
        "lift key": ItemTypes.KEY_ITEMS,
        "meteorite": ItemTypes.KEY_ITEMS,
        "mystery ticket": ItemTypes.KEY_ITEMS,
        "oak's parcel": ItemTypes.KEY_ITEMS,
        "old amber": ItemTypes.KEY_ITEMS,
        "old rod": ItemTypes.KEY_ITEMS,
        "pokeflute": ItemTypes.KEY_ITEMS,
        "powder jar": ItemTypes.KEY_ITEMS,
        "rainbow pass": ItemTypes.KEY_ITEMS,
        "ruby": ItemTypes.KEY_ITEMS,
        "sapphire": ItemTypes.KEY_ITEMS,
        "secret key": ItemTypes.KEY_ITEMS,
        "silph scope": ItemTypes.KEY_ITEMS,
        "ss ticket": ItemTypes.KEY_ITEMS,
        "super rod": ItemTypes.KEY_ITEMS,
        "tea": ItemTypes.KEY_ITEMS,
        "teachy tv": ItemTypes.KEY_ITEMS,
        "tm case": ItemTypes.KEY_ITEMS,
        "town map": ItemTypes.KEY_ITEMS,
        "tri pass": ItemTypes.KEY_ITEMS,
        "vs seeker": ItemTypes.KEY_ITEMS
    }

    def __init__(self, name):
        self.name = name
        self.type = self.ITEM_TYPES_DICT[name.lower()]
        self.sell_price = 300

        with open(join("jsons", "item_descriptions.json"), "r") as item_desc_json:
            descriptions = json.load(item_desc_json)
            self.description = descriptions[name.lower()]

    def __eq__(self, other):
        return isinstance(other, Item) and self.name == other.name

    def __hash__(self):
        """Hashing is here so that the "same" item is not added to the bag
        multiple times when using an item object as a key."""
        return hash(self.name)

