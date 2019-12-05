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
    player = Player(Vector2(32, 26), "Chris")
    poke = Pokemon("charmander")
    poke._stats["Current HP"] = 2
    poke2 = Pokemon("goldeen")
    poke3 = Pokemon("blastoise")
    poke4 = Pokemon("charizard")
    poke5 = Pokemon("dragonite")
    poke6 = Pokemon("mewtwo")
    poke6._stats["Current HP"] = 0
    poke.add_move(Move("Thunder"))
    poke.add_move(Move("Thunderbolt"))
    poke.add_move(Move("Thunder Wave"))
    poke.add_move(Move("Double Slap"))
    poke3.add_move(Move("Surf"))
    poke3.add_move(Move("Ice Beam"))
    poke3.add_move(Move("Ice Punch"))
    poke3.add_move(Move("Body Slam"))
    poke5.add_move(Move("Surf"))
    poke5.add_move(Move("Body Slam"))
    poke5.add_move(Move("Double Slap"))
    poke5.add_move(Move("Thunderbolt"))
    poke6.add_move(Move("Thunder"))
    poke6.add_move(Move("Thunderbolt"))
    poke6.add_move(Move("Thunder Wave"))
    poke6.add_move(Move("Thundershock"))

    player._pokemon_team.append(poke)
    # player._pokemon_team.append(poke2)
    # player._pokemon_team.append(poke3)
    # player._pokemon_team.append(poke4)
    # player._pokemon_team.append(poke5)
    # player._pokemon_team.append(poke6)

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
        response = game.update(ticks)
        if response == "RESTART" and running == True:
            main()
            break

if __name__ == "__main__":
   main()