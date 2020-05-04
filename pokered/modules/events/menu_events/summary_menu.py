import pygame
from os.path import join
from ...types import Types
from ...utils.managers.frameManager import FRAMES
from ...enumerated.battle_actions import BattleActions
from ...utils.text_maker import TextMaker


class SummaryMenu():
    """The summary page from the game"""
    def __init__(self, player, cursor_pos):
        """Creates the summary menu. Requires a player instead of a simple
        pokemon because it is possible to jump to the summary of other pokemon
        from the summary menu in the actual game."""
        self._is_dead = False
        self._player = player
        self._active_page = PokemonSummaryMenu(player.pokemon_team[cursor_pos])
        self._cursor_pos = cursor_pos

    def is_over(self):
        """Returns whether or not the player has exited the summary menu."""
        return self._is_dead

    def update(self, ticks):
        """Updates..."""
        self._active_page.update(ticks)

    def handle_event(self, event):
        """Handles the user input accordingly"""
        if event.key == BattleActions.UP.value:
            if self._cursor_pos >= 1:
                self._cursor_pos -= 1
                self._update_active_page()

        elif event.key == BattleActions.DOWN.value:
            if self._cursor_pos < len(self._player.pokemon_team) - 1:
                self._cursor_pos += 1
                self._update_active_page()

        elif event.key == BattleActions.BACK.value:
            self._is_dead = True
        elif event.key in [BattleActions.LEFT.value,
                           BattleActions.RIGHT.value,
                           BattleActions.SELECT.value]:
            self._active_page.handle_event(event)

    def draw(self, draw_surface):
        """Draws the active summary page"""
        self._active_page.draw(draw_surface)

    def _update_active_page(self):
        """Updates the player's active page"""
        self._active_page = \
            PokemonSummaryMenu(self._player.pokemon_team[self._cursor_pos])


class PokemonSummaryMenu():
    """Individual summary menu for a given pokemon"""
    def __init__(self, pokemon):
        self._pokemon = pokemon
        self._active_page = InfoPage(self._pokemon)

    def handle_event(self, event):
        pass

    def update(self, ticks):
        pass

    def draw(self, draw_surface):
        self._active_page.draw(draw_surface)


class InfoPage():
    """Displays a Pokemon's info page"""
    def __init__(self, pokemon):
        self._pokemon = pokemon
        self._create_page_surface()

    def handle_event(self, event):
        pass

    def update(self, ticks):
        pass

    def draw(self, draw_surface):
        """Draw all relevant information to the screen"""
        draw_surface.blit(self._page_surface, (0, 0))
        draw_surface.blit(self._pokemon.summary_image, (25, 31))
        draw_surface.blit(self._id, (168, 24))
        draw_surface.blit(self._name, (168, 39))
        draw_surface.blit(self._item, (168, 99))
        draw_surface.blit(self._train_id, (168, 84))
        draw_surface.blit(self._original_trainer, (168, 69))
        draw_surface.blit(self._memo_surface, (8, 119))
        self._type_surf.draw(draw_surface)
        if len(self._pokemon.type) > 1:
            self._type2_surf.draw(draw_surface)

    def _create_page_surface(self):
        """Creates the info page's surface that will be drawn to the screen.
        Also creates the other surfaces that need to be created to display all
        of the pokemon's info"""
        # Create info page background
        self._page_surface = FRAMES.getFrame("pokemon_info.png")

        # Create other surfaces to display on info page
        text_maker = TextMaker(join("fonts", "party_txt_font.png"))
        self._id = text_maker.get_surface(str(self._pokemon.id_num).zfill(3))
        self._name = text_maker.get_surface(self._pokemon.name.upper())
        self._item = \
            text_maker.get_surface(str(self._pokemon.held_item).upper())
        self._train_id = text_maker.get_surface(self._pokemon.trainer_id)
        self._original_trainer = \
            text_maker.get_surface(self._pokemon.original_trainer)

        # Create the type(s) surface(s)
        self._type_surf = Types(self._pokemon.type[0])
        self._type_surf._position = (167, 51)
        if len(self._pokemon.type) > 1:
            self._type2_surf = Types(self._pokemon.type[1])
            self._type2_surf._position = (202, 51)

        # Create the memo surface
        self._create_memo_surface()

    def _create_memo_surface(self):
        """Creates the trainer memo surface"""
        text_maker = TextMaker(join("fonts", "party_txt_font.png"))
        line_1 = text_maker.get_surface(self._pokemon.nature.upper() + " nature.")
        line_2 = text_maker.get_surface("Test line 2.")
        self._memo_surface = pygame.Surface((100, 30))
        self._memo_surface.fill((255, 255, 254))
        self._memo_surface.set_colorkey((255, 255, 254))
        self._memo_surface.blit(line_1, (0, 0))
        self._memo_surface.blit(line_2, (0, 14))

