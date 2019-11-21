import csv
import random
import pandas as pd
from os.path import join

class DamageCalculator:
    def __init__(self, poke_1, poke_2, weather=None):
        self._poke_1 = poke_1[0]
        self._move = poke_1[1]
        self._poke_2 = poke_2
        self._weather = weather
        self._effectiveness_string = None
        self._effectiveness = None
    
    def get_effectiveness(self):
        if self._effectiveness_string != None:
            return self._effectiveness_string
        else: return ""
    
    def get_effectiveness_sound(self):
        if self._effectiveness != None:
            return self._effectiveness
        else: return ""

    def get_damage(self):
        modifier = self.get_total_modifier()
        power = self._move.move_power
        level = self._poke_1.get_lvl()
        attack = self._poke_1._stats["Attack"] if self._move.category == "Physical" else self._poke_1._stats["Sp. Attack"]
        defense = self._poke_2._stats["Defense"] if self._move.category == "Physical" else self._poke_2._stats["Sp. Defense"]
    
        return int(((((2 * level / 5 + 2) * power * attack / defense) / 50) + 2) * modifier)

    def get_total_modifier(self):
        return round(self.get_target_modifier() * self.get_weather_modifier() * self.get_critical_modifier() * self.get_random_modifier() * self.get_stab_modifier() * self.get_type_modifier() * self.get_burn_modifier() * self.get_other_modifier(), 5)

    def get_type_modifier(self):
        df = pd.read_csv(join("csv", "type_chart.csv"))
        df = df.set_index("Attacking", drop = True)
        if len(self._poke_2.get_type()) == 2:
            mod1 = float(df.loc[self._move.move_type, self._poke_2.get_type()[0]])
            mod2 = float(df.loc[self._move.move_type, self._poke_2.get_type()[1]])
            if mod1 and mod2 == 2: 
                self._effectiveness_string, self._effectiveness = "It's super effective...", "super"
                return 4
            elif mod1 and mod2 == 0.5: 
                self._effectiveness_string, self._effectiveness = "It's not very effective...", "not"
                return 0.25
            elif (mod1 == 0.5 and mod2 == 1.5) or (mod1 == 1.5 and mod2 == 0.5): 
                self._effectiveness = "normal "
                return 1
            elif mod1 == 1 and mod2 == 1:
                self._effectiveness = "normal "
                return 1
            elif mod1 == 0 or mod2 == 0: 
                self._effectiveness_string, self._effectiveness = "It has no effect!", "none"
                return 0
            elif mod1 != 1:
                if mod1 > 1:
                    self._effectiveness_string, self._effectiveness = "It's super effective...", "super"
                else: self._effectiveness_string, self._effectiveness = "It's not very effective...", "not"
                return mod1
            elif mod2 != 1: 
                if mod2 > 1:
                    self._effectiveness_string, self._effectiveness = "It's super effective...", "super"
                else: self._effectiveness_string, self._effectiveness = "It's not very effective...", "not"
                return mod2
            else:
                print(mod1, mod2) 
                raise Exception
        else: 
            if float(df.loc[self._move.move_type, self._poke_2.get_type()[0]]) > 1:
                self._effectiveness_string, self._effectiveness = "It's super effective...", "super"
            elif float(df.loc[self._move.move_type, self._poke_2.get_type()[0]]) == 1:
                self._effectiveness = "normal"
            elif float(df.loc[self._move.move_type, self._poke_2.get_type()[0]]) < 1 and float(df.loc[self._move.move_type, self._poke_2.get_type()[0]]) > 0:
                self._effectiveness_string, self._effectiveness = "It's not very effective...", "not"
            return float(df.loc[self._move.move_type, self._poke_2.get_type()[0]])

        
    def get_target_modifier(self):
        if type(self._poke_2) != list:
            return 1
        else: return 0.5 #TODO: Implement this once moves json is made
    
    def get_weather_modifier(self):
        if self._weather == None:
            return 1
        elif self._move.move_type == "Water" and self._weather == "rain":
            return 1.5
        elif self._move.move_type == "Water" and self._weather == "harsh sunlight":
            return 0.5
        elif self._move.move_type == "Fire" and self._weather == "rain":
            return 0.5
        elif self._move.move_type == "Fire" and self._weather == "harsh sunlight":
            return 1.5
        else:
            return 1
    
    def get_critical_modifier(self):
        crit_level = 0
        if self._poke_1.get_held_item() != None and self._poke_1.get_held_item().get_item_name() in ["Razor Claw", "Scope Lens"]:
            crit_level += 1
        if self._poke_1.get_name == "Farfetch'd" and self._poke_1.get_held_item() != None and self._poke_1.get_held_item().get_item_name() == "Stick":
            crit_level += 2
        if self._poke_1.get_name == "Chansey" and self._poke_1.get_held_item() != None and self._poke_1.get_held_item().get_item_name() == "Lucky Punch":
            crit_level += 2
        
        # Crit probability
        probability = [0.0625, 0.125, 0.25, 0.333, 0.5][crit_level]
        if probability > random.random(): return 2
        else: return 1
    
    def get_random_modifier(self):
        return random.randint(85, 100) / 100
    
    def get_stab_modifier(self):
        if self._move.move_type in self._poke_1.get_type(): return 1.5
        else: return 1
    
    def get_burn_modifier(self):
        if "burn" in self._poke_1.get_status():
            if self._poke_1.get_ability() != None and self._poke_1.get_ability().get_ability_name() != "Guts":
                if self._move.category == "Physical":
                    return 0.5
        return 1
    
    def get_other_modifier(self):
        #TODO: Implement if I ever get time
        return 1
    



        

        
        


    
            
    



