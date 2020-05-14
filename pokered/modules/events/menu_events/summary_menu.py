import pygame
import json
from os.path import join

from ...types import Types
from ...utils.managers.frameManager import FRAMES
from ...enumerated.battle_actions import BattleActions
from ...utils.text_maker import TextMaker
from ...utils.misc import end_at


class SummaryMenu():
    """The summary page from the game"""
    def __init__(self, player, cursor_pos):
        """Creates the summary menu. Requires a player instead of a simple
        pokemon because it is possible to jump to the summary of other pokemon
        from the summary menu in the actual game."""
        self._is_dead = False
        self._player = player
        self._vcursor_pos = cursor_pos
        self._hcursor_pos = 0
        self._active_page = PokemonSummaryMenu(player.pokemon_team[cursor_pos],
                                               self._hcursor_pos)

    def is_over(self):
        """Returns whether or not the player has exited the summary menu."""
        return self._is_dead

    def update(self, ticks):
        """Updates..."""
        self._active_page.update(ticks)

    def handle_event(self, event):
        """Handles the user input accordingly"""
        if self._hcursor_pos == 2 and \
                self._active_page._active_page.mode == "detail":
            self._active_page.handle_event(event)

        elif event.key == BattleActions.UP.value:
            if self._vcursor_pos >= 1:
                self._vcursor_pos -= 1
                self._update_active_page()

        elif event.key == BattleActions.DOWN.value:
            if self._vcursor_pos < len(self._player.pokemon_team) - 1:
                self._vcursor_pos += 1
                self._update_active_page()

        elif event.key == BattleActions.BACK.value:
            self._is_dead = True

        elif event.key == BattleActions.LEFT.value:
            if self._hcursor_pos > 0:
                self._hcursor_pos -= 1
                self._update_active_page()

        elif event.key == BattleActions.RIGHT.value:
            if self._hcursor_pos < 2:
                self._hcursor_pos += 1
                self._update_active_page()

        elif event.key == BattleActions.SELECT.value:
            if self._hcursor_pos == 0:
                self._is_dead = True
            elif self._hcursor_pos == 2:
                self._active_page.handle_event(event)

    def draw(self, draw_surface):
        """Draws the active summary page"""
        self._active_page.draw(draw_surface)

    def _update_active_page(self):
        """Updates the player's active page"""
        self._active_page = \
            PokemonSummaryMenu(self._player.pokemon_team[self._vcursor_pos],
                               self._hcursor_pos)


class PokemonSummaryMenu():
    """Individual summary menu for a given pokemon"""
    def __init__(self, pokemon, start_pos):
        self._pokemon = pokemon
        if start_pos == 0:
            self._active_page = InfoPage(self._pokemon)
        elif start_pos == 1:
            self._active_page = StatsPage(self._pokemon)
        elif start_pos == 2:
            self._active_page = MovesPage(self._pokemon)
        self._create_general_surface()

    def handle_event(self, event):
        if type(self._active_page) is MovesPage:
            self._active_page.handle_event(event)

    def update(self, ticks):
        pass

    def _create_general_surface(self):
        """Also draws information that appears on all
        pages i.e. pokemon pic, name and level"""
        text_maker = TextMaker(join("fonts", "menu_font.png"))

        self._general_surface = pygame.Surface((150, 100))
        self._general_surface.fill((255, 255, 254))
        self._general_surface.set_colorkey((255, 255, 254))

        name_surface = text_maker.get_surface(self._pokemon.nick_name.upper())
        lvl_surface = text_maker.get_surface("Lv" +
                                             str(self._pokemon.stats["LVL"]))

        font_index = 0 if self._pokemon.gender == "male" else 1
        gender_surface = \
            FRAMES.getFrame("gender_t.png", offset=(font_index, 0))

        self._general_surface.blit(self._pokemon.summary_image, (25, 31))
        self._general_surface.blit(lvl_surface, (4, 19))
        self._general_surface.blit(name_surface, (45, 19))
        self._general_surface.blit(gender_surface, (105, 18))

    def draw(self, draw_surface):
        """Draws the active page. Also draws information that appears on all
        pages i.e. pokemon pic, name and level"""
        self._active_page.draw(draw_surface)
        if type(self._active_page) != MovesPage or \
                self._active_page.mode == "overview":
            draw_surface.blit(self._general_surface, (0, 0))


class StatsPage():
    """Displays a Pokemon's stats page"""
    def __init__(self, pokemon):
        self._pokemon = pokemon
        self._create_page_surface()

    def draw(self, draw_surface):
        """Draw all the relevant information to the screen"""
        draw_surface.blit(self._page_surface, (0, 0))
        draw_surface.blit(self._title_surface, (4, 2))

        # HP
        draw_surface.blit(self._hp_surface,
                          end_at(self._hp_surface, (236, 23)))
        draw_surface.blit(self._hp_bar_surf,
                          end_at(self._hp_bar_surf, (236, 32)))

        # Stats
        draw_surface.blit(self._attack_surface,
                          end_at(self._attack_surface, (236, 41)))
        draw_surface.blit(self._defense_surface,
                          end_at(self._defense_surface, (236, 54)))
        draw_surface.blit(self._sp_attack_surface,
                          end_at(self._sp_attack_surface, (236, 67)))
        draw_surface.blit(self._sp_defense_surface,
                          end_at(self._sp_defense_surface, (236, 80)))
        draw_surface.blit(self._speed_surface,
                          end_at(self._speed_surface, (236, 93)))

        # EXP
        draw_surface.blit(self._exp_surface,
                          end_at(self._exp_surface, (238, 108)))
        draw_surface.blit(self._nxt_exp_surface,
                          end_at(self._nxt_exp_surface, (238, 120)))
        draw_surface.blit(self._exp_bar, (end_at(self._exp_bar, (236, 129))))

        # Ability
        draw_surface.blit(self._ability_surface, (74, 133))
        draw_surface.blit(self._ability_desc_surface, (10, 145))

    def _create_page_surface(self):
        """Creates the background for page as well as surfaces for all of the
        pokemon's stats."""
        text_maker = TextMaker(join("fonts", "menu_font.png"))
        text_maker2 = TextMaker(join("fonts", "party_txt_font.png"))

        # Background and title. Need title here because this image does not
        # have it baked in unlike the info background
        self._page_surface = FRAMES.getFrame("pokemon_stats.png")
        self._title_surface = text_maker.get_surface("POKeMON SKILLS")
        self._create_hp_bar()

        # HP
        self._hp_surface = \
            text_maker2.get_surface(str(self._pokemon.stats["Current HP"]) +
                                    "/" + str(self._pokemon.stats["HP"]))

        # Stats
        self._attack_surface = \
            text_maker2.get_surface(str(self._pokemon.stats["Attack"]))
        self._defense_surface = \
            text_maker2.get_surface(str(self._pokemon.stats["Defense"]))
        self._sp_attack_surface = \
            text_maker2.get_surface(str(self._pokemon.stats["Sp. Attack"]))
        self._sp_defense_surface = \
            text_maker2.get_surface(str(self._pokemon.stats["Sp. Defense"]))
        self._speed_surface = \
            text_maker2.get_surface(str(self._pokemon.stats["Speed"]))

        # EXP
        self._exp_surface = \
            text_maker2.get_surface(str(self._pokemon.exp))
        self._nxt_exp_surface = \
            text_maker2.get_surface(str(self._pokemon.nxt_lvl))
        self._create_exp_bar()

        # Ability
        ability = self._pokemon.ability
        self._ability_surface = \
            text_maker2.get_surface(ability.name.upper())
        self._ability_desc_surface = \
            text_maker2.get_surface(ability.description.replace("é", "e"))

    def _create_hp_bar(self):
        """Add the hp bar to the pokemon box"""
        green = (112, 248, 168)
        yellow = (248, 224, 56)
        red = (241, 14, 14)

        current_hp = self._pokemon.stats["Current HP"]
        max_hp = self._pokemon.stats["HP"]
        percentage = (current_hp / max_hp)

        self._hp = pygame.Surface((int(percentage * 48), 3))
        if percentage > .50:
            self._hp.fill(green)
        elif percentage > .15:
            self._hp.fill(yellow)
        else:
            self._hp.fill(red)
        self._hp_darken = pygame.Surface((48, 1))
        self._hp_darken.fill((0, 0, 0))
        self._hp_darken.set_alpha(50)

        self._hp_bar = FRAMES.getFrame("hp_bar.png")

        # Can't blit onto the bar directly because it is a singleton
        self._hp_bar_surf = pygame.Surface((self._hp_bar.get_width(),
                                            self._hp_bar.get_height()))
        self._hp_bar_surf.fill((255, 255, 254))
        self._hp_bar_surf.set_colorkey((255, 255, 254))
        self._hp_bar_surf.blit(self._hp_bar, (0, 0))
        self._hp_bar_surf.blit(self._hp, (15, 2))

    def _create_exp_bar(self):
        """Creates the exp bar and fills it appropriately"""
        self._exp_bar = FRAMES.getFrame("exp_bar.png")
        # TODO: Implement rest of exp bar once exp system in place.


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
        line_1 = text_maker.get_surface(self._pokemon.nature.upper() +
                                        " nature.")
        line_2 = text_maker.get_surface("Test line 2.")
        self._memo_surface = pygame.Surface((100, 30))
        self._memo_surface.fill((255, 255, 254))
        self._memo_surface.set_colorkey((255, 255, 254))
        self._memo_surface.blit(line_1, (0, 0))
        self._memo_surface.blit(line_2, (0, 14))


class MovesPage():
    """Displays a pokemon's moves page"""
    def __init__(self, pokemon):
        self._pokemon = pokemon
        self.mode = "overview"
        self._vcursor_pos = 0
        self._create_page_surface()

    def handle_event(self, event):
        """Handles events. When the user first presses 'a' details of the move
        will be shown."""
        if event.key == BattleActions.SELECT.value:
            if self.mode == "overview":
                self.mode = "detail"
                self._create_page_surface()

            if self.mode == "detail":
                if self._vcursor_pos == len(self._pokemon.moves):
                    self.mode = "overview"
                    self._vcursor_pos = 0
                    self._create_page_surface()

        elif event.key == BattleActions.DOWN.value and self.mode == "detail":
            if self._vcursor_pos < len(self._pokemon.moves):
                self._vcursor_pos += 1
                self._create_move_detail_surface()

        elif event.key == BattleActions.UP.value and self.mode == "detail":
            if self._vcursor_pos > 0:
                self._vcursor_pos -= 1
                self._create_move_detail_surface()

    def draw(self, draw_surface):
        draw_surface.blit(self._page_surface, (0, 0))
        draw_surface.blit(self._title_surface, (4, 2))

        y = 21
        for move in self._moves_surfaces:
            draw_surface.blit(move, (123, y))
            y += 28

        if self.mode == "detail":
            # Draw general information about pokemon
            draw_surface.blit(self._pokemon_surface, (7, 17))
            draw_surface.blit(self._type_surf, (50, 35))
            draw_surface.blit(self._name_surf, (45, 19))
            draw_surface.blit(self._gender_surface, (105, 18))

            # Draw move stats
            draw_surface.blit(self._power_surface,
                              end_at(self._power_surface, (75, 60)))
            draw_surface.blit(self._accuracy_surface,
                              end_at(self._accuracy_surface, (75, 74)))
            draw_surface.blit(self._effect_surface, (6, 102))

            # Draw moves selector
            draw_surface.blit(self._selector,
                              (120, 18 + self._vcursor_pos * 28))

            # Draw cancel button
            draw_surface.blit(self._cancel, (167, 138))

    def _create_page_surface(self):
        """Creates the move page's surface which will be drawn to the page.
        Will also create all other info needed to draw the page."""
        # Create the page's background.
        if self.mode == "overview":
            self._page_surface = FRAMES.getFrame("pokemon_moves.png")
        else:
            self._page_surface = FRAMES.getFrame("pokemon_moves_active.png")
            self._create_move_active_general_surface()
            self._create_move_detail_surface()

        text_maker = TextMaker(join("fonts", "party_txt_font.png"))
        text_maker2 = TextMaker(join("fonts", "menu_font.png"))

        # Create title surface
        self._title_surface = text_maker2.get_surface("KNOWN MOVES")

        # Creates a surface for each move that exists
        self._moves_surfaces = []

        for move in self._pokemon.moves:
            # Create surface for move
            surface = pygame.Surface((130, 30))
            surface.fill((255, 255, 254))
            surface.set_colorkey((255, 255, 254))

            # Create info for move
            type_surf = Types(move.move_type)
            name_surf = text_maker.get_surface(move.move_name.upper())
            pp_surf = text_maker.get_surface("PP" + str(move.current_pp) +
                                             "/" + str(move.max_pp))

            # Add info to surface
            type_surf.draw(surface)
            surface.blit(name_surf, (40, 3))
            surface.blit(pp_surf, end_at(pp_surf, (114, 15)))

            # Add surface to move surface list
            self._moves_surfaces.append(surface)

    def _create_move_active_general_surface(self):
        """When a move is being analyzed the left half of the menu changes and
        it is necessary to override the information drawn in PokemonSummary
        Menu."""
        # Create small pokemon image surface
        with open(join("jsons", "pokemon_lookup_s.json"), "r") as \
                pokemon_lookup_json:
            pokemon_lookup = json.load(pokemon_lookup_json)
            lookup = pokemon_lookup[self._pokemon.name]

        offset = (0, lookup)
        self._pokemon_surface = \
            FRAMES.getFrame(join("pokemon", "pokemon_small.png"),
                            offset=offset)

        # Create types surface
        self._type_surf = pygame.Surface((80, 20))
        self._type_surf.fill((255, 255, 254))
        self._type_surf.set_colorkey((255, 255, 254))

        x = 0
        for poke_type in self._pokemon.type:
            type_surf_subset = Types(poke_type)
            type_surf_subset._position = (x, 0)
            type_surf_subset.draw(self._type_surf)
            x += 35

        # Create name surface
        text_maker = TextMaker(join("fonts", "menu_font.png"))
        self._name_surf = text_maker.get_surface(self._pokemon.nick_name)

        # Create gender surface
        font_index = 0 if self._pokemon.gender == "male" else 1
        self._gender_surface = \
            FRAMES.getFrame("gender_t.png", offset=(font_index, 0))

    def _create_move_detail_surface(self):
        """Creates surfaces containing details about a move.
        (Power, accuracy, effect)"""
        text_maker = TextMaker(join("fonts", "party_txt_font.png"), max=115,
                               line_height=14)
        if self._vcursor_pos == len(self._pokemon.moves):
            # Clear surfaces
            self._power_surface = text_maker.get_surface("")
            self._accuracy_surface = text_maker.get_surface("")
            self._effect_surface = text_maker.get_surface("")

        else:
            move = self._pokemon.moves[self._vcursor_pos]
            self._power_surface = text_maker.get_surface(str(move.move_power))
            self._accuracy_surface = text_maker.get_surface(str(move.accuracy))
            self._effect_surface = text_maker.get_surface(str(move.effects))

        self._selector = FRAMES.getFrame("moves_selector.png")
        self._cancel = text_maker.get_surface("CANCEL")
