import pygame
import os
from modules.vector2D import Vector2
from modules.drawable import Drawable
from modules.player import Player
from modules.battle import Battle

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

    # Let's make a background so we can see if we're moving
    background = Drawable("gym.png", Vector2(0, 0))
   
    # Images
    player = Player(Vector2(WORLD_SIZE[0]//2 - 8, WORLD_SIZE[1]//2 - 11))
   
    # Define a variable to control the main loop
    running = True
    game_clock = pygame.time.Clock()
    battle = Battle(player, player, draw_surface)
   
   
    # Main loop
    while running:
        if battle == None:
            # Draw everything, based on the offset
            background.draw(draw_surface)
            player.draw(draw_surface)
            pygame.transform.scale(draw_surface, UPSCALED, screen)
            pygame.display.flip()
            
            # event handling, gets all event from the eventqueue
            game_clock.tick(60)
            for event in pygame.event.get():
                # only do something if the event is of type QUIT or ESCAPE is pressed
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    # change the value to False, to exit the main loop
                    running = False
                if (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_b]:
                    player.move(event)

            # Update everything
            ticks = game_clock.get_time() / 1000
            player.update(ticks)

            # Update Offset

            

        else:
            running = battle.battle_loop(game_clock, UPSCALED, screen, running)


        
        


   
if __name__ == "__main__":
   main()