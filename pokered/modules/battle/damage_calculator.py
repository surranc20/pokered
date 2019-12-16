import csv
import random
import pandas as pd
from os.path import join

class DamageCalculator:
    def __init__(self, poke_1, poke_2, weather=None):
        """Creates a battle damage calculator. Poke_1 is a tuple containing the attacking 
        pokemon and the move that it used. Poke2 is the defending pokemon. The weather is the current
        weather status of the battle."""
        self._poke_1 = poke_1[0]
        self._move = poke_1[1]
        self._poke_2 = poke_2
        self._weather = weather
        # Returns a string stating how effective a move was.
        self._effectiveness_string = None
        # Returns how effective the move was so that the correct impact sound can be played.
        self._effectiveness = None

    def get_effect(self):
        """Calculate whether a moves effect (example would be if thunder paralysis the hit pokemon) happens and return the effect."""
        prob = random.randint(0, 100)
        if prob > self._move.effect_accuracy:
            return None
        else:
            if self._move.effects in ["paralyze"]:
                return self._move.effects
            else: return None

    
    def get_effectiveness(self):
        """Return the string representing how effective a move was. An example would be: 'It was super effective!'"""
        if self._effectiveness_string != None:
            return self._effectiveness_string
        else: return ""
    
    def get_effectiveness_sound(self):
        """Return a string determining how effective a move was so the correct sound can be played in the battle_fsm. 
        Differentiates from get_effectiveness() because this method would only return 'super' as opposed to the long
        string in the example above."""
        if self._effectiveness != None:
            return self._effectiveness
        else: return ""

    def get_damage(self):
        """Gets the damage a move will do based on the formula listed here: https://bulbapedia.bulbagarden.net/wiki/Damage"""
        if self._move.move_name == "Dragon Rage":
            self.type_modifier()
            return 40
        if self._move.category == "Status":
            return 0
        modifier = self.get_total_modifier()
        power = self._move.move_power
        level = self._poke_1.get_lvl()
        attack = self._poke_1.stats["Attack"] if self._move.category == "Physical" else self._poke_1.stats["Sp. Attack"]
        defense = self._poke_2.stats["Defense"] if self._move.category == "Physical" else self._poke_2.stats["Sp. Defense"]
    
        return int(((((2 * level / 5 + 2) * power * attack / defense) / 50) + 2) * modifier)

    def get_total_modifier(self):
        """Calculates the modifier variable in the damage equation."""
        return round(self.get_target_modifier() * self.get_weather_modifier() * self.get_critical_modifier() * self.get_random_modifier() * self.get_stab_modifier() * self.type_modifier() * self.get_burn_modifier() * self.get_other_modifier(), 5)

    def type_modifier(self):
        """Determine how effective a move is based on the type of the move and the defending pokemon."""
        df = pd.read_csv(join("csv", "type_chart.csv"))
        df = df.set_index("Attacking", drop = True)
        # If the defending pokemon has two types things get a little more complicated. 
        if len(self._poke_2.type) == 2:
            # The following variables represent the effect modifier for each type
            mod1 = float(df.loc[self._move.move_type, self._poke_2.type[0]])
            mod2 = float(df.loc[self._move.move_type, self._poke_2.type[1]])
            # If the move is super effective agaisnt both types than the move is super super effective.
            if mod1 and mod2 == 2: 
                self._effectiveness_string, self._effectiveness = "It's super effective...", "super"
                return 4
            # If the move is not very effective against both types than the move is barely effective.
            elif mod1 and mod2 == 0.5: 
                self._effectiveness_string, self._effectiveness = "It's not very effective...", "not"
                return 0.25
            # If the move is super effective against one type and not very effective against the other type
            # then the modifiers cancel eachother out.
            elif (mod1 == 0.5 and mod2 == 1.5) or (mod1 == 1.5 and mod2 == 0.5): 
                self._effectiveness = "normal"
                return 1
            elif mod1 == 1 and mod2 == 1:
                self._effectiveness = "normal"
                return 1
            elif mod1 == 0 or mod2 == 0: 
                self._effectiveness_string, self._effectiveness = "It has no effect!", "none"
                return 0
            
            # The following are all cases where one of the modifiers is 1 and the other is not.
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
                # Simply here to ensure the above logic is correct. Should never trigger.
                print(mod1, mod2) 
                raise Exception

        # When the defending pokemon only has one type the calculation is much easier.
        else: 
            if float(df.loc[self._move.move_type, self._poke_2.type[0]]) > 1:
                self._effectiveness_string, self._effectiveness = "It's super effective...", "super"
            elif float(df.loc[self._move.move_type, self._poke_2.type[0]]) == 1:
                self._effectiveness = "normal"
            elif float(df.loc[self._move.move_type, self._poke_2.type[0]]) < 1 and float(df.loc[self._move.move_type, self._poke_2.type[0]]) > 0:
                self._effectiveness_string, self._effectiveness = "It's not very effective...", "not"
            return float(df.loc[self._move.move_type, self._poke_2.type[0]])

        
    def get_target_modifier(self):
        """Moves are less effective if they are targeted at both pokemon in a double battle."""
        if type(self._poke_2) != list:
            return 1
        else: return 0.5 
    
    def get_weather_modifier(self):
        """Get the weather modifier for a move and the current weather."""
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
        """Determine whether or not a move was a critical hit."""
        crit_level = 0
        if self._poke_1.held_item != None and self._poke_1.held_item.get_item_name() in ["Razor Claw", "Scope Lens"]:
            crit_level += 1
        if self._poke_1.get_name == "Farfetch'd" and self._poke_1.held_item != None and self._poke_1.held_item.get_item_name() == "Stick":
            crit_level += 2
        if self._poke_1.get_name == "Chansey" and self._poke_1.held_item != None and self._poke_1.held_item.get_item_name() == "Lucky Punch":
            crit_level += 2
        
        # Crit probability
        probability = [0.0625, 0.125, 0.25, 0.333, 0.5][crit_level]
        if probability > random.random(): return 2
        else: return 1
    
    def get_random_modifier(self):
        """The damage calculator has a little randomness thrown in."""
        return random.randint(85, 100) / 100
    
    def get_stab_modifier(self):
        """Calculate STAB modifier. Stands for Same Type Attack Boost."""
        if self._move.move_type in self._poke_1.type: return 1.5
        else: return 1
    
    def get_burn_modifier(self):
        """Using a pysical move while burned usually lowers the damage dealt."""
        if "burn" in self._poke_1.get_status():
            if self._poke_1.get_ability() != None and self._poke_1.get_ability().get_ability_name() != "Guts":
                if self._move.category == "Physical":
                    return 0.5
        return 1
    
    def get_other_modifier(self):
        #TODO: Implement if I ever get time
        return 1
    