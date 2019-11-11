import pygame
import os
from modules.utils.vector2D import Vector2
from modules.utils.drawable import Drawable
from modules.player import Player
from modules.battle.battle import Battle
from modules.pokemon import Pokemon
from modules.move import Move
from modules.battle.damage_calculator import DamageCalculator
from modules.utils.game_manager import GameManager

# Two different sizes now! Screen size is the amount we show the player,
#  and world size is the size of the interactable world.
WORLD_SIZE = (208, 203)
SCREEN_SIZE = (240, 160)
SCALE = 3
UPSCALED = [x * SCALE for x in SCREEN_SIZE]


def main():
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    pygame.display.set_caption("Pokemon Gym")
    screen = pygame.display.set_mode(UPSCALED)
    draw_surface = pygame.Surface(SCREEN_SIZE)
   
    # Create Player and Enemy for Test Battle
    player = Player(Vector2(WORLD_SIZE[0]//2 - 8, WORLD_SIZE[1]//2 - 11), "Chris")
    enemy = Player(Vector2(WORLD_SIZE[0]//2 - 8, WORLD_SIZE[1]//2 - 11), "CHAMPION GARY", enemy=True)
    enemy._pokemon_team.append(Pokemon("charizard", enemy=True))
    enemy._pokemon_team.append(Pokemon("pikachu", enemy=True))
    enemy._pokemon_team.append(Pokemon("charizard", enemy=True))
    poke = Pokemon("pikachu")
    poke2 = Pokemon("bulbasaur")
    poke3 = Pokemon("mankey")
    poke4 = Pokemon("charizard")
    poke5 = Pokemon("pidgeot")
    poke6 = Pokemon("mew")
    poke.add_move(Move("Thunder"))
    poke.add_move(Move("Thunder"))
    poke.add_move(Move("Thunder"))
    poke.add_move(Move("Thunder"))

    player._pokemon_team.append(poke)
    player._pokemon_team.append(poke2)
    player._pokemon_team.append(poke3)
    player._pokemon_team.append(poke4)
    player._pokemon_team.append(poke5)
    player._pokemon_team.append(poke6)

    # Make game variable
    game = GameManager(SCREEN_SIZE, player)
   
    # Define a variable to control the main loop
    running = True
    game_clock = pygame.time.Clock()
   
    # Main loop
    while running:
        # Draw everything from level
        game.draw(draw_surface)
        pygame.transform.scale(draw_surface, UPSCALED, screen)
        pygame.display.flip()
        
        # event handling, gets all event from the event queue
        game_clock.tick(60)
        for event in pygame.event.get():
            # only do something if the event is of type QUIT or ESCAPE is pressed
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # change the value to False, to exit the main loop
                running = False
            if (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
                game.handle_event(event)

        # Update everything
        ticks = game_clock.get_time() / 1000
        game.update(ticks)

if __name__ == "__main__":
   main()