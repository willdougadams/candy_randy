import pygame
import math

from skill import Skill

class AOE(Skill):
  def fire(self, position):
    if self.cooldown_countdown <= 0 and not self.fired:
      self.center = tuple(map(int, position))
      self.fired = True
      return self

    return None
