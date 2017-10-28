import pygame
import math

class Aura():
  BLACK = (0, 0, 0)
  WHITE = (255, 255, 255)
  BLUE  = (0, 0, 255)
  GREEN = (0, 255, 0)
  RED = (255, 0, 0)

  def __init__(self, caster, screen, r=65):
    self.fired = False
    self.target_dest = (50, 50)
    self.screen = screen
    self.caster = caster
    self.center = (1, 1)
    self.r = r
    self.warmup_color = Aura.GREEN
    self.active_color = Aura.BLACK
    self.draw_color = self.warmup_color
    self.cooldown_countdown = 160
    self.warmup_countdown = 1
    self.active_countdown = 120
    self.damage_per_tick = 2

  def update(self, pcs, npcs):
    if self.cooldown_countdown > 0:
      self.cooldown_countdown -= 1

    if not self.fired:
      return

    if self.warmup_countdown > 0:
      self.warmup_countdown -= 1
      if self.warmup_countdown == 0:
        self.draw_color = self.active_color
    else:
      self.center = self.caster.center
      self.active_countdown -= 1
      for pc in pcs:
        if self.collide_point(pc.center) and pc is not self.caster:
          pc.take_damage(self.damage_per_tick)
      for npc in npcs:
        if self.collide_point(npc.center):
          npc.take_damage(self.damage_per_tick)

  def draw(self):
    pygame.draw.circle(self.screen, self.draw_color, self.center, self.r)

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

  def collide_point(self, coord):
    x1, y1 = self.center
    x2, y2 = coord
    dist = abs(math.hypot(x2 - x1, y2 - y1))
    return dist < self.r
