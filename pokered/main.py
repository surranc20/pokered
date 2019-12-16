import pygame
from modules.utils.vector2D import Vector2
from modules.player import Player
from modules.pokemon import Pokemon
from modules.move import Move
from modules.utils.stat_calc import StatCalculator
from modules.utils.managers.game_manager import GameManager

# Two different sizes now! Screen size is the amount we show the player,
#  and world size is the size of the interactable world.
SCREEN_SIZE = (240, 160)
SCALE = 3
UPSCALED = [x * SCALE for x in SCREEN_SIZE]


def main():
    """Sets up the game and runs game loop."""
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    pygame.display.set_caption("Pokemon Gym")
    screen = pygame.display.set_mode(UPSCALED)
    draw_surface = pygame.Surface(SCREEN_SIZE)

    # Create Player and add pokemon to their team
    player = Player(Vector2(32, 26), "Chris")
    poke = Pokemon("pikachu")
    poke2 = Pokemon("mewtwo")
    poke3 = Pokemon("blastoise")
    poke4 = Pokemon("onix")
    poke5 = Pokemon("dragonite")
    poke6 = Pokemon("mew")
    poke6.stats["Current HP"] = 0
    poke.add_move(Move("Thunder"))
    poke.add_move(Move("Thunderbolt"))
    poke.add_move(Move("Thunder Wave"))
    poke.add_move(Move("Double Slap"))
    poke2.add_move(Move("Thunder"))
    poke2.add_move(Move("Thunderbolt"))
    poke2.add_move(Move("Thunder Wave"))
    poke2.add_move(Move("Double Slap"))

    poke3.add_move(Move("Surf"))
    poke3.add_move(Move("Ice Beam"))
    poke3.add_move(Move("Ice Punch"))
    poke3.add_move(Move("Body Slam"))
    poke4.add_move(Move("Rock Tomb"))
    poke4.add_move(Move("Earthquake"))
    poke4.add_move(Move("Iron Tail"))
    poke4.add_move(Move("Body Slam"))
    poke5.add_move(Move("Surf"))
    poke5.add_move(Move("Body Slam"))
    poke5.add_move(Move("Double Slap"))
    poke5.add_move(Move("Thunderbolt"))
    poke6.add_move(Move("Thunder"))
    poke6.add_move(Move("Ice Punch"))
    poke6.add_move(Move("Body Slam"))
    poke6.add_move(Move("Thunder Wave"))

    stat_calc = StatCalculator()
    poke.stats = stat_calc.calculate_main(poke, 65)
    poke2.stats = stat_calc.calculate_main(poke2, 60)
    poke3.stats = stat_calc.calculate_main(poke3, 51)
    poke4.stats = stat_calc.calculate_main(poke4, 58)
    poke5.stats = stat_calc.calculate_main(poke5, 53)
    poke6.stats = stat_calc.calculate_main(poke6, 70)

    player.pokemon_team.append(poke)
    player.pokemon_team.append(poke2)
    player.pokemon_team.append(poke3)
    player.pokemon_team.append(poke4)
    player.pokemon_team.append(poke5)
    player.pokemon_team.append(poke6)

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
            # Catch quit events
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             event.key == pygame.K_ESCAPE):
                # change the value to False, to exit the main loop
                running = False
            if (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
                game.handle_event(event)

        # Update everything
        ticks = game_clock.get_time() / 1000
        response = game.update(ticks)
        if response == "RESTART" and running:
            main()
            break


if __name__ == "__main__":
    main()
