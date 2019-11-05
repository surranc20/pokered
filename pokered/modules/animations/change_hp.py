from ..battle_menus.poke_info import PokeInfo

class ChangeHP(PokeInfo):
    def __init__(self, pokemon, damage, enemy=False):
        super().__init__(pokemon, enemy)
        self._start_hp = pokemon._stats["Current HP"]
        self._current_hp = self._start_hp
        self._new_hp = self._start_hp - damage
    
    def update(self, ticks):
        print(self.is_dead(), self._current_hp, self._new_hp)
        if int(self._current_hp) != int(self._new_hp):
            print("happening")
            super().__init__(self._pokemon, self._enemy, self._current_hp - 1)
        else: self.kill()
    
    def is_dead(self):
        return self._is_dead
    


        
