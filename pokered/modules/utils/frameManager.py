import pygame
from pygame import image, Surface, Rect
from os.path import join


class FrameManager(object):
   """A singleton factory class to create and store frames on demand."""
   
   # The singleton instance variable
   _INSTANCE = None
   
   @classmethod
   def getInstance(cls):
      """Used to obtain the singleton instance"""
      if cls._INSTANCE == None:
         cls._INSTANCE = cls._FM()
      
      return cls._INSTANCE
   
   # Do not directly instantiate this class!
   class _FM(object):
      """An internal FrameManager class to contain the actual code. Is a private class."""
      
      # Folder in which images are stored
      _IMAGE_FOLDER = "images"
      
      # Static information about the frame sizes of particular image sheets.
      _FRAME_SIZES = {
         "trainer.png" : (16, 22),
         "party_active_poke_bar.png" : (84, 57),
         "party_individual_poke_bar.png" : (150, 24),
         "party_cancel_bar.png" : (54, 24),
         "party_text_box.png" : (180, 28),
         "menu.png" : (62, 46),
         "gender.png" : (5, 8),
         join("battle" ,"battle_background.png") : (240, 112),
         join("battle" ,"battle_menus.png") : (240, 48),
         join("battle", "trainer_toss_anim.png") : (64, 64),
         join("battle", "pokeball_anim.png") : (16, 16),
         join("battle", "pokeball_open_anim.png") : (16, 16),
         join("battle", "health_bars.png") : (108, 42),
         join("battle", "pokemon_remaining_balls.png") : (7, 7),
         join("battle", "pokemon_remaining.png") : (104, 12),
         join("battle", "cursor.png") : (8, 12),
         join("pokemon", "pokemon_small.png") : (32,32),
         join("trainers", "lorelei.png") : (16,22),
         join("trainers", "bruno.png") : (16,22),
         join("moves", "thunder.png") : (32, 32),
         join("moves", "thunderbolt.png") : (16, 32),
         join("moves", "thunderbolt_ball.png") : (32, 32),
         join("moves", "thunderbolt_static.png") : (16, 16),
         join("moves", "thunder_background.png") : (480, 112), 
         "pokemon_fire_red_battle_font.png" : (5, 9),
         "party_txt_font.png" : (5, 9),
         "party_font.png" : (5, 8),
         "text_cursor.png" : (12, 8)
         

      }
      
      # A default frame size
      _DEFAULT_FRAME = (64,64)
      
      # A list of images that require to be loaded with transparency
      _TRANSPARENCY = [join("battle" ,"battle_menus.png")]
      
      # A list of images that require to be loaded with a color key
      _COLOR_KEY = [join("moves", "thunderbolt_static.png"), join("moves", "thunderbolt_ball.png"), join("moves", "thunderbolt.png"), join("moves", "thunder.png"), join("trainers", "bruno.png"), join("trainers", "bruno_b.png"), "text_cursor.png", join("trainers", "lorelei.png"), join("trainers", "lorelei_b.png"), "gender.png", "menu.png", "trainer.png", "party_text_box.png", "party_cancel_bar.png", join("pokemon", "pokemon_small.png"), join("battle", "trainer_toss_anim.png"), join("battle", "pokeball_anim.png"), join("battle", "pokeball_open_anim.png"), join("pokemon", "pokemon_big.png"), join("battle", "health_bars.png"), join("trainers", "lorelei_b.png") ,join("battle", "gary_battle.png"), "pokemon_fire_red_battle_font.png", join("battle", "pokemon_remaining_balls.png"), join("battle", "pokemon_remaining.png"), join("battle", "cursor.png"), "party_active_poke_bar.png", "party_individual_poke_bar.png"]
      
      
      
      def __init__(self):
         # Stores the surfaces indexed based on file name
         # The values in _surfaces can be a single Surface
         #  or a two dimentional grid of surfaces if it is an image sheet
         self._surfaces = {}
      
      
      def __getitem__(self, key):
         return self._surfaces[key]
   
      def __setitem__(self, key, item):
         self._surfaces[key] = item
      
      
      def getFrame(self, fileName, offset=None):
         # If this frame has not already been loaded, load the image from memory
         if fileName not in self._surfaces.keys():
            self._loadImage(fileName, offset != None)
         
         # If this is an image sheet, return the correctly offset sub surface
         if offset != None:
            return self[fileName][offset[1]][offset[0]]
         
         # Otherwise, return the sheet created
         return self[fileName]
      
      def _loadImage(self, fileName, sheet=False):
         # Load the full image
         try:
            fullImage = image.load(join(FrameManager._FM._IMAGE_FOLDER, fileName))
         except Exception as e:
            print(e)
            print()
            fullImage = image.load(join("levels", fileName))
         
         # Look up some information about the image to be loaded
         transparent = fileName in FrameManager._FM._TRANSPARENCY
         colorKey = fileName in FrameManager._FM._COLOR_KEY
         
         # Detect if a transparency is needed
         if transparent or "level_foreground" in fileName:
            fullImage = fullImage.convert_alpha()
         else:
            fullImage = fullImage.convert()
         
         # If the image to be loaded is an image sheet, split it up based on the frame size
         if sheet:
               
            self[fileName] = []
            spriteSize = FrameManager._FM._FRAME_SIZES.get(fileName, FrameManager._FM._DEFAULT_FRAME)
            
            sheetDimensions = fullImage.get_size()
            
            for y in range(0, sheetDimensions[1], spriteSize[1]):
               self[fileName].append([])
               for x in range(0, sheetDimensions[0], spriteSize[0]):
                  
                  # If we need transparency
                  if transparent:
                     frame = Surface(spriteSize, pygame.SRCALPHA, 32)
                  else:
                     frame = Surface(spriteSize)
                     
                  frame.blit(fullImage, (0,0), Rect((x,y), spriteSize))
                  
                  # If we need to set the color key
                  if colorKey:
                     frame.set_colorkey(frame.get_at((0,0)))
                  
                  self[fileName][-1].append(frame)
         else:
            
            self[fileName] = fullImage
               
            # If we need to set the color key
            if colorKey:
               self[fileName].set_colorkey(self[fileName].get_at((0,0)))
         
      def reload(self, fileName, offset=False):
         """This is a hack that I currently need becuase of the way PokeInfo is implemented. 
         It resets the surfaces for a given filename"""
         self._surfaces.pop(fileName)
         return self.getFrame(fileName, offset=offset)

               
            
         
         
# Set up an instance for others to import         
FRAMES = FrameManager.getInstance()