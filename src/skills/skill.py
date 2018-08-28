import pygame
import math

class Skill:
  BLACK = (0, 0, 0)
  WHITE = (255, 255, 255)
  BLUE  = (0, 0, 255)
  GREEN = (0, 255, 0)
  RED = (255, 0, 0)

  def __init__(self, caster, screen, r=10):
    self.fired = False
    self.alive = True
    self.target_dest = (0, 0)
    self.center = (0, 0)
    self.screen = screen
    self.caster = caster
    self.r = r
    self.x_speed = 0
    self.y_speed = 0
    self.move_speed = 100
    self.draw_color = Skill.GREEN
    self.warmup_color = Skill.GREEN
    self.active_color = Skill.BLACK
    self.warmup_countdown = 10
    self.cooldown_countdown = 10
    self.damage_per_tick = 10
    self.active_countdown = float('inf')

  def update(self, pcs, npcs, elapsed, damage_maps):
    if self.cooldown_countdown > 0:
      self.cooldown_countdown -= 1
      return

    if not self.fired:
      return

    current_x, current_y = self.center
    new_x = current_x + (self.x_speed * elapsed)
    new_y = current_y + (self.y_speed * elapsed)
    new_coord = (new_x, new_y)
    self.center = new_coord

    if self.warmup_countdown > 0:
      self.warmup_countdown -= 1
      if self.warmup_countdown == 0:
        self.draw_color = self.active_color
      return

    self.active_countdown -= 1
    if self.active_countdown < 0:
      self.alive = False
      return

    for pc in pcs:
      if self.collide_point(pc.center) and pc is not self.caster:
        pc.take_damage(self.damage_per_tick)

    for npc in npcs:
      if self.collide_point(npc.center):
        npc.take_damage(self.damage_per_tick)

    for damage_type, surf in damage_maps.iteritems():
      center = (int(self.center[0]), int(self.center[1]))
      pygame.draw.circle(self.screen, self.draw_color, center, self.r)

  def draw(self):
    center = (int(self.center[0]), int(self.center[1]))
    pygame.draw.circle(self.screen, self.draw_color, center, self.r)

  '''
  AOE.fire() will return itself to indicate that it is available for use,
  otherwise None. This passes control of the Skill from the PC which created it
  to Game.active_skills[]
  '''
  def fire(self, position):
    raise NotImplementedError("[!!] Skill with no firing method defined")

  def collide_point(self, coord):
    x1, y1 = self.center
    x2, y2 = coord
    dist = abs(math.hypot(x2 - x1, y2 - y1))
    return dist < self.r
