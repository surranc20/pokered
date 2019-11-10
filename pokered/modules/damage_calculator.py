import csv
import pandas as pd

class DamageCalculator:
    def __init__(self, poke_1, poke_2):
        self._poke_1 = poke_1
        self._poke_2 = poke_2


    def get_type_modifier(self):
        df = pd.read_csv("type_chart.csv")
        df = df.set_index("Attacking", drop = True)
        return float(df.loc[self._poke_1.get_type("Electric"), self._poke_2.get_type("Steel")])
        
    def get_target_modifier(self):
        if type(self._poke_2) != list:
            return 0
        else: pass


