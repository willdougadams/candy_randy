import pygame
import math

from skill import Skill
from core.util import colors

class Swing(Skill):
  def __init__(self, caster, skill_filename, reach):
    Skill.__init__(self, caster, skill_filename)
    self.r = reach
    self.direction_dict = {
      0: (math.radians(250), math.radians(290)),
      1: (math.radians(160), math.radians(200)),
      2: (math.radians(340), math.radians(20)),
      3: (math.radians(70), math.radians(110))
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
    start, end = self.direction_dict[self.caster.orientation]
    mid = (start+end)/2

    w, h = self.image.get_size()
    screen.blit(self.image, (self.center[0], self.center[1]))#, (self.center[0], self.center[1], w, h))
    pygame.draw.arc(
                screen,
                self.current_color,
                (self.center[0]-self.r, self.center[1]-self.r, self.r*2, self.r*2),
                start,
                end,
                self.r
              )

    if self.image is not None:
      x, y = self.center[0]-self.height/2, self.center[1]-self.width/2
      x = int(x)
      y = int(y)
      screen.blit(self.image, (x, y), (0, 0, self.width, self.height))

  def draw_damage(self, damage_maps):
    start, end = self.direction_dict[self.caster.orientation]
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
