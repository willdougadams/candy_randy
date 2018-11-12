import pygame
import math

from core.util import read_config, colors

class Skill:
  def __init__(self, caster, skill_filename):
    self.fired = False
    self.alive = True
    self.target_dest = (0, 0)
    self.center = (float(0), float(0))
    self.caster = caster
    config = read_config('res/Skills/'+skill_filename)
    self.r = float(config['radius'])
    self.warmup_countdown = float(config['warmup_time'])
    self.cooldown_countdown = float(config['cooldown_time'])
    self.active_countdown = float(config['active_time'])
    self.move_speed = float(config['move_speed'])
    self.dps = float(config['dps'])
    self.current_color = self.warmup_color = colors.BLUE
    self.active_color = (self.dps, float(0), float(0))
    self.x_speed = 0
    self.y_speed = 0

  def update(self, elapsed):
    if self.cooldown_countdown > float(0.0):
      self.cooldown_countdown -= elapsed
      return

    if not self.fired:
      return

    current_x, current_y = self.center
    new_x = current_x + (self.x_speed * elapsed)
    new_y = current_y + (self.y_speed * elapsed)
    new_coord = (new_x, new_y)
    self.center = new_coord

    if self.warmup_countdown > 0:
      self.warmup_countdown -= elapsed
      if self.warmup_countdown <= 0:
        self.current_color = self.active_color
      return

    self.active_countdown -= elapsed
    if self.active_countdown <= 0:
      self.alive = False
      return

  def draw_damage(self, damage_maps):
    for damage_type, surf in damage_maps.iteritems():
      center = (int(self.center[0]), int(self.center[1]))
      pygame.draw.circle(surf, self.current_color, center, int(self.r))

    return damage_maps

  def draw(self, screen):
    center = (int(self.center[0]), int(self.center[1]))
    pygame.draw.circle(screen, self.current_color, center, int(self.r))

  '''
  When implemented, Skill.fire() will return itself to indicate that it is available for use,
  otherwise None. This passes control of the Skill from the PC which created it
  to Game.active_skills[]
  '''
  def fire(self, position):
    raise NotImplementedError("[!!] You must define this skill's fire() method")

  def collide_point(self, coord):
    x1, y1 = self.center
    x2, y2 = coord
    dist = abs(math.hypot(x2 - x1, y2 - y1))
    return dist < self.r
