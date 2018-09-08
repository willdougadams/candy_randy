import pygame
import math

from skill import Skill

class Attack(Skill):
  def update(self, elapsed):
    Skill.update(self, elapsed)
    self.center = self.caster.center

  def fire(self, position):
    if self.cooldown_countdown <= 0 and not self.fired:
      self.center = position
      self.fired = True
      return self

    return None
