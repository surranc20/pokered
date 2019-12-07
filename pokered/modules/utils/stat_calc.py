import json
from os.path import join
import random

"""This module was coded by my brother Kolbe Surran. User name shockedeel on github"""
class StatCalculator:
    def __init__(self):
        print("initialized")

    def calculate_main(self,pokemon, lvl):
        new_stat={}
        with open(join("jsons", "pokemon.json"), "r") as pokemonfile:
            pokemon_j = json.load(pokemonfile)
            print(pokemon._name)
            base_hp=pokemon_j[pokemon._name.capitalize()]["base"]["HP"]
            base_attack=pokemon_j[pokemon._name.capitalize()]["base"]["Attack"]
            base_defense=pokemon_j[pokemon._name.capitalize()]["base"]["Defense"]
            base_sp_attack=pokemon_j[pokemon._name.capitalize()]["base"]["Sp. Attack"]
            base_sp_defense=pokemon_j[pokemon._name.capitalize()]["base"]["Sp. Defense"]
            base_speed=pokemon_j[pokemon._name.capitalize()]["base"]["Speed"]
            
            hp = self.calculate_hp(base_hp, lvl)
            attack = self.calculate_stat_other(base_attack, lvl)
            defense = self.calculate_stat_other(base_defense, lvl)
            sp_attack = self.calculate_stat_other(base_sp_attack, lvl)
            sp_defense = self.calculate_stat_other(base_sp_defense, lvl)
            speed = self.calculate_stat_other(base_speed, lvl)
            new_stats= {"LVL": lvl,
            "HP":hp,
            "Current HP":hp,
            "Attack":attack,
            "Defense":defense,
            "Sp. Attack":sp_attack,
            "Sp. Defense":sp_defense,
            "Speed":speed
        }
        print(new_stats)
        return new_stats
            
            
            
        
    def calculate_hp(self,base_hp,lvl):
        iv=random.randint(1,33)
        ev=random.randint(1,33)
        return int(((2*base_hp+iv+(ev/4))*lvl) /100 +lvl+10)



    def calculate_stat_other(self,base_stat,level):
        iv=random.randint(1,33)
        ev=random.randint(1,33)
        nature=1
        return int(((((2*base_stat+iv+(ev/4))*level)/100)+5)*nature)

