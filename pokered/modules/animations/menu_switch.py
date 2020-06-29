from ..battle.battle_menus.poke_party import ActivePokemon, SecondaryPokemon


class MenuSwitch():
    def __init__(self, slot1, slot1_index, slot2, slot2_index):
        """Menu switch animation displayed when the player swaps the position
        of pokemon in the menu. Slot1 and Slot2 are ActivePokemon or
        SecondaryPokemon instances. Slot1_index and Slot2_index are the
        indices of slot1 and slot2 in the selectedable_items list from the
        menu."""
        self.slot1 = slot1
        self.slot1_index = slot1_index
        self.slot2 = slot2
        self.slot2_index = slot2_index
        self._first_stage_over = False
        self._is_dead = False
        self._delta_remaining = 160
        self._delta = 4

    def is_dead(self):
        """Returns whether or not the animation is finished."""
        return self._is_dead

    def update(self, ticks):
        """Updates the position of slot1 and slot2."""
        if self._delta_remaining > 0:
            # Adjust slot1's position based on whether or not it is an
            # ActivePokemon or SecondaryPokemon.
            if type(self.slot1) is ActivePokemon:
                self.slot1._position = (self.slot1._position[0] - self._delta,
                                        self.slot1._position[1])
                self.slot1._bouncing_pokemon._position = \
                    (self.slot1._bouncing_pokemon._position[0] - self._delta,
                     self.slot1._bouncing_pokemon._position[1])
            else:
                self.slot1._position = (self.slot1._position[0] + self._delta,
                                        self.slot1._position[1])
                self.slot1._bouncing_pokemon._position = \
                    (self.slot1._bouncing_pokemon._position[0] + self._delta,
                     self.slot1._bouncing_pokemon._position[1])

            # Adjust slot2's position based on whether or not it is an
            # ActivePokemon or SecondaryPokemon.
            if type(self.slot2) is ActivePokemon:
                self.slot2._position = (self.slot2._position[0] - self._delta,
                                        self.slot2._position[1])
                self.slot2._bouncing_pokemon._position = \
                    (self.slot2._bouncing_pokemon._position[0] - self._delta,
                     self.slot2._bouncing_pokemon._position[1])
            else:
                self.slot2._position = (self.slot2._position[0] + self._delta,
                                        self.slot2._position[1])
                self.slot2._bouncing_pokemon._position = \
                    (self.slot2._bouncing_pokemon._position[0] + self._delta,
                     self.slot2._bouncing_pokemon._position[1])

            self._delta_remaining -= abs(self._delta)

        # Animation is either done or first stage is done.
        else:
            if not self._first_stage_over:
                self._first_stage_over = True
                self._delta = -1 * self._delta
                self._delta_remaining = 160

                # Switch the positions of the two pokemon bars
                temp = self.slot1._position
                temp_bounce = self.slot1._bouncing_pokemon._position
                self.slot1._position = self.slot2._position
                self.slot1._bouncing_pokemon._position = \
                    self.slot2._bouncing_pokemon._position
                self.slot2._position = temp
                self.slot2._bouncing_pokemon._position = temp_bounce

                # If either pokemon is an active pokemon then switch the types
                # of slot1 and slot2.
                if type(self.slot1) is ActivePokemon:
                    self.slot1 = SecondaryPokemon(self.slot1._pokemon,
                                                  self.slot1._position,
                                                  selected=True,
                                                  second_green=True)
                    self.slot2 = ActivePokemon(self.slot2._pokemon,
                                               self.slot2._position,
                                               selected=True,
                                               green=True)

                elif type(self.slot2) is ActivePokemon:
                    self.slot1 = ActivePokemon(self.slot1._pokemon,
                                               self.slot1._position,
                                               selected=True,
                                               second_green=True)
                    self.slot2 = SecondaryPokemon(self.slot2._pokemon,
                                                  self.slot2._position,
                                                  selected=True,
                                                  green=True)

            # If the first stage had already been completed and their is no
            # delta remaining then the animation is over.
            else:
                self._is_dead = True
