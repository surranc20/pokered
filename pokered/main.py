import pygame
import pickle
import json
import logging
from os.path import join
from modules.utils.vector2D import Vector2
from modules.player import Player
from modules.pokemon import Pokemon
from modules.move import Move
from modules.utils.stat_calc import StatCalculator
from modules.utils.managers.game_manager import GameManager
from modules.utils.managers.controller_manager import ControllerManager

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

    # Load config file
    with open(join("jsons", "config.json"), "r") as json_config:
        config_data = json.load(json_config)
        use_controller = bool(config_data["controller"])

    try:
        if use_controller:
            joystick = pygame.joystick.Joystick(0)
            controller_manager = ControllerManager(joystick, 0.2)
            if not joystick.get_init():
                joystick.init()
    except pygame.error:
        print("WARNING: Controller loading failed...")
        use_controller = False

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
    poke.stats = stat_calc.calculate_main(poke, 99)
    poke2.stats = stat_calc.calculate_main(poke2, 60)
    poke2.stats["Current HP"] = 0
    poke3.stats = stat_calc.calculate_main(poke3, 51)
    poke4.stats = stat_calc.calculate_main(poke4, 58)
    poke5.stats = stat_calc.calculate_main(poke5, 53)
    poke6.stats = stat_calc.calculate_main(poke6, 70)

    player.add_pokemon(poke)
    player.set_active_pokemon(0)
    player.add_pokemon(poke2)
    player.add_pokemon(poke3)
    player.add_pokemon(poke4)
    #player.add_pokemon(poke5)
    #player.add_pokemon(poke6)


    # Make game variable
    try:
        with open("savegame", "rb") as f:
            game = pickle.load(f)
            game.load = True
    except Exception as e:
        print(e)
        game = GameManager(SCREEN_SIZE, player)

    # Define a variable to control the main loop
    running = True
    game_clock = pygame.time.Clock()

    # Create logger
    logging.basicConfig(filename="log.log",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    logger = logging.getLogger("Main Logger")
    handler = logging.FileHandler("log.log")
    logger.addHandler(handler)




    # Main loop
    while running:
        # Draw everything from level
        game.draw(draw_surface)
        pygame.transform.scale(draw_surface, UPSCALED, screen)
        pygame.display.flip()

        # event handling, gets all event from the event queue
        game_clock.tick(60)
        for event in pygame.event.get():

            # Check if the user has a controller plugged in and convert events
            # to keyboard events if they do have one plugged in.
            if use_controller and event.type == pygame.JOYAXISMOTION:

                event_data = controller_manager.get_joystick_data()

                # If the event is not valid (joystick held in same direction)
                # then don't process event.
                if not controller_manager.input_valid:
                    break

                # Create event from event data
                event = pygame.event.Event(event_data[0], event_data[1])

            if use_controller and event.type == pygame.JOYBUTTONDOWN:
                event_data = controller_manager.get_button_data(event)
                if not controller_manager.input_valid:
                    break
                event = pygame.event.Event(2, event_data)

            # Catch quit events
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             event.key == pygame.K_ESCAPE):
                # change the value to False, to exit the main loop
                running = False
            if (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
                if event.key == pygame.K_m:
                    pygame.mixer.music.pause()
                game.handle_event(event)

        # Update everything
        ticks = game_clock.get_time() / 1000
        response = game.update(ticks)
        fps = game_clock.get_fps()
        # print(fps)
        if fps < 55:
            logger.info(fps)

        if response == "RESTART" and running:
            main()
            break
        if response == "Pickle" and running:
            print("yooooo")
            with open("savegame", "wb") as f:
                pickle.dump(game, f)


if __name__ == "__main__":
    main()
