from .give_event import SubEvent
from ...enumerated.battle_actions import BattleActions


class TakeEvent(SubEvent):
    def __init__(self, pokemon, bag):
        self.pokemon = pokemon
        self.bag = bag
        self.display_pokemon_menu = True
        self.is_dead = False

        # Check the pokemon's held item and see if their is room in the bag.
        item = self.pokemon.held_item
        if item is not None and self.bag[item.type].get(item, 0) < 999:
            self.can_take = True
        else:
            self.can_take = False

        # Create the string to display in the grame based on item and if their
        # is room.
        if item is None:
            first_string = f"{pokemon.name.upper()} isn't holding anything."
        elif self.can_take:
            first_string = (f"Recieved the {item.name.upper()} from "
                            f"{pokemon.name.upper()}.")
        else:
            first_string = (f"The BAG is full. The POKéMON's item could "
                            f"not be removed.")

        super().__init__(pokemon, None, bag, first_string)

    def handle_event(self, event):
        if event.key == BattleActions.SELECT.value:
            self.is_dead = True
            if self.can_take:
                item = self.pokemon.held_item
                self.pokemon.held_item = None
                self.bag.add_item(item)
