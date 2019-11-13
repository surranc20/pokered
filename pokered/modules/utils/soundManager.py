"""
A Singleton Sound Manager class
Author: Liz Matthews, 9/20/2019

Provides on-demand loading of sounds for a pygame program.

"""


import pygame
import os


class SoundManager(object):
   """A singleton factory class to create and store sounds on demand."""
   
   # The singleton instance variable
   _INSTANCE = None
   
   @classmethod
   def getInstance(cls):
      """Used to obtain the singleton instance"""
      if cls._INSTANCE == None:
         cls._INSTANCE = cls._SM()
      
      return cls._INSTANCE
   
   # Do not directly instantiate this class!
   class _SM(object):
      """An internal SoundManager class to contain the actual code. Is a private class."""
      
      # Folders in which sounds are stored
      _MUSIC_FOLDER = os.path.join("music")
      _SFX_FOLDER = os.path.join("sounds")
      
      _FOLDER = {
         "firered_0005.wav"     : _SFX_FOLDER,
         "firered_0007.wav"     : _SFX_FOLDER,
         "gym_music.wav"        : _MUSIC_FOLDER
      }
      
      
      
      def __init__(self):
         # 
         if not pygame.mixer.get_init():
            pygame.mixer.init()
            
         self._sounds = {}
         self._music = {}
         self._musicStatus = "stop" # or "play" or "pause"
      
      def playSound(self, fileName, loop=0, sound=None):
         # Plays the requested sound effect, default only once
         if fileName not in self._sounds.keys():
            self._load(fileName)
         if sound != None:
            self._sounds[fileName].set_volume(sound)
               
         return self._sounds[fileName].play(loop)
      
      def playMusic(self, fileName, loop=0, sound=1):
         if self._musicStatus != "stop":
            self.stopMusic()
         pygame.mixer.music.load(os.path.join(SoundManager._SM._MUSIC_FOLDER, fileName))
         pygame.mixer.music.set_volume(sound)
         pygame.mixer.music.play()
         
         self._musicStatus = "play"
      
      def stopMusic(self):
         pygame.mixer.music.stop()
         
         self._musicStatus = "stop"
      
      def togglePlayMusic(self, fileName, loop=0):
         if self._musicStatus == "stop":
            self.playMusic(fileName, loop)
         
         elif self._musicStatus == "play":
            self.stopMusic()
      
      def togglePauseMusic(self):
         if self._musicStatus == "play":
            self.pauseMusic()
         elif self._musicStatus == "pause":
            self.unpauseMusic()
      
      def pauseMusic(self):
         if self._musicStatus == "play":
            pygame.mixer.music.pause()
            
            self._musicStatus = "pause"
      
      def unpauseMusic(self):
         if self._musicStatus == "pause":
            pygame.mixer.music.unpause()
         
            self._musicStatus = "play"
               
      
      def stopSound(self, fileName):
         self._sounds[fileName].stop()
         
      def stopChannel(self, channel):
         channel.stop()
      
      def pauseChannel(self, channel):
         channel.pause()
      
      def unpauseChannel(self, channel):
         channel.unpause()
      
      def stopSoundAll(self):
         pygame.mixer.stop()
      
      def pauseSoundAll(self):
         pygame.mixer.pause()
      
      def unpauseSoundAll(self):
         pygame.mixer.unpause()
      
      def stopAll(self):
         self.stopSoundAll()
         self.stopMusic()
      
      def pauseAll(self):
         self.pauseSoundAll()
         self.pauseMusicAll()
      
      def unpauseAll(self):
         self.unpauseSoundAll()
         self.unpauseMusicAll()
      
         
      
      def updateVolumePositional(self, channel, relativePosition, soundPosition, distance=300, minVolume=0.2):
         
         if (channel.get_busy()):
         
            distanceDiff = relativePosition.x - soundPosition.x
                              
            if distanceDiff < 0:
               
               channel.set_volume(max(minVolume, (distance + distanceDiff) / distance),
                                  1)
            else:
               channel.set_volume(1,
                                  max(minVolume, (distance - distanceDiff) / distance))
         
     
      def _load(self, fileName):
         self._sounds[fileName] = pygame.mixer.Sound(os.path.join(SoundManager._SM._FOLDER.get(fileName,
                                                                                               SoundManager._SM._MUSIC_FOLDER),
                                                                  fileName))
               
            
         