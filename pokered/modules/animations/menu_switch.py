from ..battle.battle_menus.poke_party import ActivePokemon, SecondaryPokemon


class MenuSwitch():
    def __init__(self, slot1, slot1_index, slot2, slot2_index):
        self.slot1 = slot1
        self.slot1_index = slot1_index
        self.slot2 = slot2
        self.slot2_index = slot2_index
        self._first_stage_over = False
        self._is_dead = False
        self._delta_remaining = 160
        self._delta = 4

    def is_dead(self):
        return self._is_dead

    def update(self, ticks):
        if self._delta_remaining > 0:
            if type(self.slot1) is ActivePokemon:
                self.slot1._position = (self.slot1._position[0] - self._delta, self.slot1._position[1])
                self.slot1._bouncing_pokemon._position = (self.slot1._bouncing_pokemon._position[0] - self._delta, self.slot1._bouncing_pokemon._position[1])
            else:
                self.slot1._position = (self.slot1._position[0] + self._delta, self.slot1._position[1])
                self.slot1._bouncing_pokemon._position = (self.slot1._bouncing_pokemon._position[0] + self._delta, self.slot1._bouncing_pokemon._position[1])
            if type(self.slot2) is ActivePokemon:
                self.slot2._position = (self.slot2._position[0] - self._delta, self.slot2._position[1])
                self.slot2._bouncing_pokemon._position = (self.slot2._bouncing_pokemon._position[0] - self._delta, self.slot2._bouncing_pokemon._position[1])
            else:
                self.slot2._position = (self.slot2._position[0] + self._delta, self.slot2._position[1])
                self.slot2._bouncing_pokemon._position = (self.slot2._bouncing_pokemon._position[0] + self._delta, self.slot2._bouncing_pokemon._position[1])

            self._delta_remaining -= abs(self._delta)
        else:
            if not self._first_stage_over:
                self._first_stage_over = True
                self._delta = -1 * self._delta
                self._delta_remaining = 160
                temp = self.slot1._position
                temp_bounce = self.slot1._bouncing_pokemon._position
                self.slot1._position = self.slot2._position
                self.slot1._bouncing_pokemon._position = self.slot2._bouncing_pokemon._position
                self.slot2._position = temp
                self.slot2._bouncing_pokemon._position = temp_bounce

                if type(self.slot1) is ActivePokemon:
                    self.slot1 = SecondaryPokemon(self.slot1._pokemon, self.slot1._position, selected=True, second_green=True)
                    self.slot2 = ActivePokemon(self.slot2._pokemon, self.slot2._position, selected=True, green=True)
                elif type(self.slot2) is ActivePokemon:
                    self.slot1 = ActivePokemon(self.slot1._pokemon, self.slot1._position, selected=True, second_green=True)
                    self.slot2 = SecondaryPokemon(self.slot2._pokemon, self.slot2._position, selected=True, green=True)





            else:
                self._is_dead = True



