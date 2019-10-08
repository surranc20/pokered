from os.path import join
import pygame
from ..frameManager import FRAMES
from ..animated import AnimatedGroupPart
from ..vector2D import Vector2



class PokeEmerge(AnimatedGroupPart):

    PLAYER_POKE_POS = Vector2(78, 112)
    ENEMY_POKE_POS = Vector2(180, 70)
    POKEMON_LOOKUP = {"bulbasaur":(0,0), "charmander":(2,0), "squirtle":(4,0), "caterpie":(6,0), "weedle":(8,0), "golem":(10,0), "slowpoke":(12,0), "magneton":(14,0), "dodrio":(16,0), "grimer":(18,0),
    "ivysaur":(0,1), "charmeleon":(2,1), "wartortle":(4,1), "metapod":(6,1), "kakuna":(8,1), "ponyta":(10,1), "slowbro":(12,1), "farfetch'd":(14,1), "seel":(16,1), "muk":(18,1),
    "venusaur":(0,2), "charazard":(2,2), "blastoise":(4,2), "butterfree":(6,2), "beedrill":(8,2), "rapidash":(10,2), "magnemite":(12,2), "doduo": (14,2), "dewgong":(16,2), "shellder":(18,2),
    "pidgy":(0,3), "rattata":(2,3), "fearow":(4,3), "pikachu":(6,3), "sandslash":(8,3), "cloyster":(10,3), "gengar":(12,3), "hypno":(14,3), "voltorb":(16,3), "exeggutor":(18,3),
    "pidgeotto":(0,4), "raticate":(2,4), "ekans":(4,4), "raichu":(6,4), "nidoran_g":(8,4), "gastly":(10,4), "onyx":(12,4), "krabby":(14,4), "electrode":(16,4), "cubone":(18,4),
    "pidgeot":(0,5), "spearow":(2,5), "arbok":(4,5), "sandshrew":(6,5), "nidorina":(8,5), "haunter":(10,5), "drowsee":(12,5), "kingler":(14,5), "exeggcute":(16,5), "marowak":(18,5),
    "nidoqueen":(0,6), "nidoking":(2,6), "vulpix":(4,6), "wigglytuff":(6,6), "oddish":(8,6), "hitmonlee":(10,6), "koffing":(12,6), "rhydon":(14,6), "kangaskhan":(16,6), "goldeen":(18,6),
    "nidoran_b":(0,7), "clefairy":(2,7), "ninetails":(4,7), "zubat":(6,7), "gloom":(8,7), "hitmonchan":(10,7), "weezing":(12,7), "chansey":(14,7), "horsea":(16,7), "seaking":(18,7),
    "nidorino":(0,8), "clefable":(2,8), "jigglypuff":(4,8), "golbat":(6,8), "vileplum":(8,8), "lickitung":(10,8), "rhyhorn":(12,8), "tangela":(14,8), "seadra":(16,8), "staryu":(18,8),
    "paras":(0,9), "venomoth":(2,9), "meowth":(4,9), "golduck":(6,9), "growlithe":(8,9), "starmie":(10,9), "jynx":(12,9), "pinser":(14,9), "gyrados":(16,9), "eevee":(18,9),
    "parasect":(0,10), "diglett":(2,10), "persian":(4,10), "mankey":(6,10), "arcanine":(8,10), "mr. mime":(10,10), "electabuzz":(12,10), "taurus":(14,10), "lapras":(16,10), "vaporeon":(18,10),
    "venonat":(0,11), "dugtrio":(2,11), "pysduck":(4,11) , "primeape":(6,11), "poliwag":(8,11), "scyther":(10,11), "magmar":(12,11), "magikarp":(14,11), "ditto":(16,11), "jolteon":(18,11),
    "poliwhirl":(0,12), "kadabra":(2,12), "machoke":(4,12), "weepinbell":(6,12), "tentacruel":(8,12), "flareon":(10,12), "omastar":(12,12), "aerodactyl":(14,12), "zapdos":(16,12), "dragonair":(18,12),
    "poliwrath":(0,13), "alakazam":(2,13), "machamp":(4,13), "victreebel":(6,13), "geodude":(8,13), "porygon":(10,13), "kabuto":(12,13), "snorlax":(14,13), "moltres":(16,13), "dragonite":(18,13),
    "abra":(0,14), "machop":(2,14), "bellsprout":(4,14), "tentacool":(6,14), "graveler":(8,14), "omanyte":(10,14), "kabutops":(12,14), "articuno":(14,14), "dratini":(16,14), "mewtwo":(18,14),
    "mew":(0,15)}

    def __init__(self, position, pokemon_name, anim_sequence_pos, thrower = "player"):
        _lookup = self.POKEMON_LOOKUP[pokemon_name]
        _offset = _lookup if thrower != "player" else (_lookup[0] + 1, _lookup[1])
        super().__init__(join("pokemon", "pokemon_big.png"), position, anim_sequence_pos, offset=_offset)
        self._thrower = "player"
        self._frame = 1
        self._orig_image = self._image.copy()
        
        self._anim_started = False
        self._nFrames = 2
        self._animate = True
        self._framesPerSecond = 40

        self._image = self.scale_pokemon()
    
    def __repr__(self):
        return "poke emerge"
    
    def update(self, ticks):
        if self._animate:
            self._animationTimer += ticks

        if self._animationTimer > 1 / self._framesPerSecond:
            self._animationTimer -= 1 / self._framesPerSecond
            self._image = self.scale_pokemon()
            
    def _update_position(self, copy):
        if self._thrower == "player": pos = self.PLAYER_POKE_POS
        else: pos = self.ENEMY_POKE_POS

        self._position.x = pos.x  - copy.get_width() // 2
        self._position.y = pos.y - copy.get_height()



    def scale_pokemon(self):
        if not self._anim_started:
            next_scale_size = 8
        else:
            next_scale_size = self._image.get_height() + 8

        if next_scale_size >= 64 and self._anim_started: 
            self._update_position(self._orig_image)
            self.kill()
            return self._orig_image
    
        
        self._anim_started = True
        copy = pygame.transform.scale(self._orig_image, (next_scale_size, next_scale_size))
        self._update_position(copy)
        pygame.transform.threshold(copy, copy, self._image.get_colorkey(), set_color=(244, 189, 244))
        return  copy

        





    




    
        
        
