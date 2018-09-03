import pygame
import math

from skill import Skill

class Bolt(Skill):
  def fire(self, position):
    if self.cooldown_countdown <= 0 and not self.fired:
      src_x, src_y = self.center = self.caster.center
      dst_x, dst_y = position
      delta_x = dst_x - src_x
      delta_y = dst_y -  src_y

      theta = math.atan2(delta_y, delta_x)
      self.y_speed = math.sin(theta) * self.move_speed
      self.x_speed = math.cos(theta) * self.move_speed

      self.fired = True
      return self
    else:
      return None
