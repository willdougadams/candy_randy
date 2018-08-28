import pygame
import math

from skill import Skill

class AOE(Skill):
  def __init__(self, caster, screen, r=50):
    Skill.__init__(self, caster, screen)
    self.fired = False
    self.target_dest = (50, 50)
    self.screen = screen
    self.caster = caster
    self.center = (1, 1)
    self.r = r
    self.warmup_color = Skill.GREEN
    self.active_color = Skill.BLACK
    self.draw_color = self.warmup_color
    self.cooldown_countdown = 120
    self.warmup_countdown = 120
    self.active_countdown = 120
    self.damage_per_tick = 1

  '''
  AOE.fire() will return itself to indicate that it is available for use,
  otherwise None. This passes control of the Skill from the PC which created it
  to Game.active_skills[]
  '''
  def fire(self, position):
    if self.cooldown_countdown == 0 and not self.fired:
      self.center = tuple(map(int, position))
      self.fired = True
      return self

    return None
