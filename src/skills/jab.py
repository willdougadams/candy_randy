import pygame
import math
import logging

from skill import Skill
from core.util import colors

class Jab(Skill):
  def __init__(self, caster, skill_filename, reach):
    Skill.__init__(self, caster, skill_filename)
    self.r = reach
    self.direction_dict_rad = {
      0: (math.radians(250), math.radians(290)),
      1: (math.radians(160), math.radians(200)),
      2: (math.radians(340), math.radians(380)),
      3: (math.radians(70), math.radians(110))
    }
    self.direction_dict_deg = {
      0: 180,
      1: 90,
      2: 270,
      3: 0
    }
    self.direction_offsets = {
      0:(0, 0),
      1:(0, 0),
      2:(0, 0),
      3:(0, 0)
    }
    self.image = None

  def update(self, elapsed):
    Skill.update(self, elapsed)
    self.center = self.caster.center
    self.height = self.width = 16

  def fire(self, position):
    if self.cooldown_countdown <= 0 and not self.fired:
      self.fired = True
      return self

  def draw(self, screen):
    if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
      start, end = self.direction_dict_rad[self.caster.orientation]
      mid = (start+end)/2
      w, h = self.image.get_size()
      pygame.draw.arc(
                  screen,
                  self.current_color,
                  (self.center[0]-self.r, self.center[1]-self.r, self.r*2, self.r*2),
                  start,
                  end,
                  self.r
                )

    if self.image is not None:
      angle = self.direction_dict_deg[self.caster.orientation]
      img = pygame.transform.rotate(self.image, angle)
      x, y = self.center[0]-self.height/2, self.center[1]-self.width/2
      x = int(x)
      y = int(y)
      x_offset, y_offset = self.direction_offsets[self.caster.orientation]
      screen.blit(img, (x+x_offset, y+y_offset), (0, 0, img.get_width(), img.get_height()))

  def draw_damage(self, damage_maps):
    start, end = self.direction_dict_rad[self.caster.orientation]
    for damage_type, surf in damage_maps.iteritems():
      center = (int(self.center[0]), int(self.center[1]))
      pygame.draw.arc(
                surf,
                self.current_color,
                (center[0]-self.r, center[1]-self.r, self.r*2, self.r*2),
                start,
                end,
                self.r
              )

    return damage_maps

  def set_image(self, new_image):
    self.image = new_image
    self.direction_offsets = {
      0:(-self.image.get_width()*0.2, self.image.get_height()*0.6),
      1:(-self.image.get_width()*0.8, 0),
      2:(self.image.get_width()*0.8, 0),
      3:(0, -self.image.get_height()*0.8)
    }
