import json
from os.path import join


class Ability():
    """Abilities, introduced in Generation 3 (Ruby/Sapphire), are special
    attributes given to each Pokémon that can aid them in battle. Many
    abilities act as a "power-up" by increasing a move or stat; others
    introduce a third-party effect like a weather condition. Some abilities
    can even hinder a Pokémon battle. Each Pokémon can have only one ability,
    however, some have the option of two different abilities. The choice is
    random and each ability is equally likely."""
    def __init__(self, ability_name):
        """Creates the ability of the given name. Looks up the ability
        description and stores it."""
        with open(join("jsons", "abilities.json"), "r") as abilities_json:
            abilities = json.load(abilities_json)

        if ability_name not in abilities:
            raise KeyError(ability_name)

        self.name = ability_name
        self.description = abilities[ability_name]
