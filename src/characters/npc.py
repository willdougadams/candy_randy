import pygame

from pc import PC
from random import randint
import math

target_location = (0, 0)

class NPC(PC):
  def __init__(self, coord, r, screen, npc_filename, level):
    PC.__init__(self, coord, r, screen, npc_filename, level)
    self.spritesheet_x = self.width * int(self.attrib_dict["spritesheet_position"][0])
    self.spritesheet_y = self.height * int(self.attrib_dict["spritesheet_position"][1])
    self.step = 0.0
    self.current_sprite_index = 0
    self.level = level

  def npc_update(self, elapsed, damage_maps):
    if not self.alive:
      return

    self.step += elapsed
    if self.step > 0.5:
      self.current_sprite_index = (self.current_sprite_index + 1) % 2
      self.step = 0.0

    self.curr_sprite_sheet = self.sprite_sheets[self.current_sprite_index]

    self.image.blit(self.curr_sprite_sheet,
                    (0, 0),
                    (self.spritesheet_x, self.spritesheet_y, self.width, self.height)
                  )

    #for damage_type, surf in damage_maps.iteritems():
    #  pygame.draw.circle(surf, (0, 1, 0), self.center, self.width)

    self.apply_damage(elapsed, damage_maps)

  def apply_damage(self, elapsed, damage_maps):
    # npcs take damage with red and do damage with green
    for damage_type, surf in damage_maps.iteritems():
      damage_done = surf.get_at(tuple(map(int, self.center))).r
      damage_done *= elapsed
      self.take_damage(damage_done)

  def draw_damage_to_maps(self, damage_maps):
    for damage_type, surf in damage_maps.iteritems():
      pygame.draw.circle(surf, (0, 10, 0), self.center, self.width)

    return damage_maps