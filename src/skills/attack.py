import pygame
import math

from skill import Skill

class Attack(Skill):
  BLACK = (0, 0, 0)
  WHITE = (255, 255, 255)
  BLUE  = (0, 0, 255)
  GREEN = (0, 255, 0)
  RED = (255, 0, 0)

  def __init__(self, caster, screen, r=65):
    Skill.__init__(self, caster, screen)
    self.fired = False
    self.target_dest = (50, 50)
    self.screen = screen
    self.caster = caster
    self.center = (1, 1)
    self.r = r
    self.warmup_color = Attack.GREEN
    self.active_color = Attack.BLACK
    self.draw_color = self.warmup_color
    self.cooldown_countdown = 100
    self.warmup_countdown = 1
    self.active_countdown = 250
    self.damage_per_tick = 20

  '''
  Aura.fire() will return itself to indicate that it is available for use,
  otherwise None. This passes control of the Skill from the PC which created it
  to Game.active_skills[]
  '''
  def fire(self, position):
    if self.cooldown_countdown == 0 and not self.fired:
      self.center = position
      self.fired = True
      return self

    return None
