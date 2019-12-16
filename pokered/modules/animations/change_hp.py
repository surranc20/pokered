from ..battle.battle_menus.poke_info import PokeInfo
from ..utils.managers.soundManager import SoundManager

class ChangeHP(PokeInfo):
    """This is the animation that plays while the pokemon's health bar slowly goes down.
    This is necessary becuase the health bar does not simply drop all at once. It slowly
    goes down."""
    def __init__(self, pokemon, damage, sound, enemy=False):
        super().__init__(pokemon, pokemon.enemy)
        self._start_hp = pokemon.stats["Current HP"]
        self._current_hp = self._start_hp
        self._new_hp = max(self._start_hp - damage, 0)
        if sound == "super":
            SoundManager.getInstance().playSound("firered_000E.wav")
        if sound == "not":
            SoundManager.getInstance().playSound("firered_000C.wav")
        if sound == "normal":
            SoundManager.getInstance().playSound("firered_000D.wav")


    def update(self, ticks):
        """Achieves the animation effect by decrementing a counter by one and creating a new poke info
        with hp set to that counter. Once all damage has been accounted for the animation is over."""
        if int(self._current_hp) != int(self._new_hp):
            super().__init__(self._pokemon, self._enemy, self._current_hp - 1)
        else:
            self._pokemon.stats["Current HP"] = self._new_hp
            self.kill()

    def is_dead(self):
        """Returns whether or not the animation is over"""
        return self._is_dead




