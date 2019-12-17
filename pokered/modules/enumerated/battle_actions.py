from enum import Enum
import pygame


class BattleActions(Enum):
    """Simple Enumeration of battle actions"""
    SELECT = pygame.K_RETURN
    BACK = pygame.K_b
    UP = pygame.K_w
    LEFT = pygame.K_a
    DOWN = pygame.K_s
    RIGHT = pygame.K_d