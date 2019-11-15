from ..battle.battle_menus.poke_info import PokeInfo

class ChangeHP(PokeInfo):
    def __init__(self, pokemon, damage, enemy=False):
        super().__init__(pokemon, pokemon._enemy)
        self._start_hp = pokemon._stats["Current HP"]
        self._current_hp = self._start_hp
        self._new_hp = max(self._start_hp - damage, 0)
    
    def update(self, ticks):
        if int(self._current_hp) != int(self._new_hp):
            super().__init__(self._pokemon, self._enemy, self._current_hp - 1)
        else:
            self._pokemon._stats["Current HP"] = self._new_hp
            self.kill()
    
    def is_dead(self):
        return self._is_dead
    


        
