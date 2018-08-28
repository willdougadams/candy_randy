import pygame
import math

from skill import Skill

class Bolt(Skill):
  BLACK = (0, 0, 0)
  WHITE = (255, 255, 255)
  BLUE  = (0, 0, 255)
  GREEN = (0, 255, 0)
  RED = (255, 0, 0)

  def __init__(self, caster, screen, r=10):
    Skill.__init__(self, caster, screen)
    self.fired = False
    self.target_dest = (0, 0)
    self.center = (0, 0)
    self.screen = screen
    self.caster = caster
    self.r = r
    self.x_speed = 0
    self.y_speed = 0
    self.move_speed = 100
    self.draw_color = Bolt.GREEN
    self.cooldown_countdown = 10
    self.damage_per_tick = 10
    self.active_countdown = float('inf')

  '''
  AOE.fire() will return itself to indicate that it is available for use,
  otherwise None. This passes control of the Skill from the PC which created it
  to Game.active_skills[]
  '''
  def fire(self, position):
    if self.cooldown_countdown == 0 and not self.fired:
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
