from pc import PC
from random import randint
import math

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
      self.current_sprite_index = (self.current_sprite_index + 1) %  2
      self.step = 0.0

    self.curr_sprite_sheet = self.sprite_sheets[self.current_sprite_index]

    move_speed = self.move_speed * elapsed
    seed = randint(1, 100)
    x_pos = self.center[0]
    y_pos = self.center[1]

    if seed == 1:
      x_pos += move_speed
    elif seed == 2:
      x_pos -= move_speed
    elif seed == 3:
      y_pos += move_speed
    elif seed == 4:
      y_pos -= move_speed

    self.center = (x_pos, y_pos)

    self.image.blit(self.curr_sprite_sheet,
                    (0, 0),
                    (self.spritesheet_x, self.spritesheet_y, self.width, self.height)
                  )

    for damage_type, surf in damage_maps.iteritems():
      damage_done = surf.get_at(tuple(map(int, self.center))).r * elapsed
      self.take_damage(damage_done)
