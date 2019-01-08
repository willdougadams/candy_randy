import pygame
import math

from core.util import read_config, colors
from skill import Skill

class Attack(Skill):
  def __init__(self, caster, skill_filename):
    self.fired = False
    self.alive = True
    self.target_dest = (0, 0)
    self.center = (float(0), float(0))
    self.caster = caster
    config = read_config(skill_filename)
    self.r = float(config['radius'])
    self.dps = 0

    self.warmup_countdown = 0.001
    self.cooldown_countdown = 0.25
    self.active_countdown = 0.25

    self.move_speed = 0
    self.current_color = self.warmup_color = colors.BLUE
    self.active_color = (self.dps, float(0), float(0))
    self.x_speed = 0
    self.y_speed = 0

  def update(self, elapsed):
    Skill.update(self, elapsed)
    self.center = self.caster.center

  def fire(self, position, dps):
    damages = [v for _, v in dps.iteritems()]
    damage = sum(damages) / len(damages)
    self.set_dps(damage)
    if self.cooldown_countdown <= 0 and not self.fired:
      self.center = position
      self.fired = True
      return self