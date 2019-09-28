from enum import Enum

class Cardinality(Enum):
    """Simple Enumeration of Cardinality that helps to track character orientation"""
    NORTH = 1
    SOUTH = 0
    EAST = 2
    WEST = -2