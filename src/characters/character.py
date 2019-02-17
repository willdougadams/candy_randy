import pygame

import pygame
import logging
from skills.aoe import AOE
from skills.bolt import Bolt
from skills.aura import Aura
from skills.jab import Jab
from items.inventory import Inventory
from items.gear import Gear
from core.util import read_config, colors, RUNTIME_LOG_LEVEL


class Character:
  def __init__(self, coord, r, buffer_frame, filename, level):
    self.attrib_dict = read_config(filename)
    w, h = pygame.display.get_surface().get_size()
    self.center = coord
    self.target_dest = coord
    self.level = level
    self.orientation = 0
    self.step = 0
    self.location_grid_space = self.level.surf_to_grid(self.center)#int(self.center[1]/len(self.level.grid)), int(self.center[0]/len(self.level.grid[0]))
    self.visible_tiles = self.level.get_fov(self.location_grid_space, self.orientation)
    self.r = r
    self.width = int(self.attrib_dict["sprite_width"])
    self.height = int(self.attrib_dict["sprite_height"])
    self.spritesheet_x = 0
    self.spritesheet_y = 0
    self.collection_radius = 15
    self.moved = True
    self.gear = Gear()

    self.alive_color = colors.BLUE
    self.dead_color = colors.BLACK
    self.draw_color = self.alive_color
    self.move_speed = int(self.attrib_dict['move_speed'])
    self.attack = Jab(self, 'res/Skills/Swing.skill', self.gear.get_reach())
    self.attack.set_image(self.gear.get_attack_image())
    self.max_speed = 15

    '''
    skills[] will hold the actual skill objects, and will refill skill
    slots appropriatly using skill_types, which is a list of the constructors
    '''
    self.skills = []
    self.skill_types = [AOE, Bolt, Aura]
    self.skill_files = ['res/Skills/AOE.skill', 'res/Skills/Bolt.skill', 'res/Skills/Aura.skill']
    self.attack_file = 'res/Skills/Swing.skill'
    for i, skill_type in enumerate(self.skill_types):
      self.skills.append(skill_type(self, self.skill_files[i]))

    self.active_skill = 0
    self.health_points = int(self.attrib_dict["health"])
    self.alive = True

    self.inventory = Inventory()
    self.sprite_sheets = []
    for sheetname in self.attrib_dict["spritesheets"]:
      self.sprite_sheets.append(pygame.image.load("res/DawnLike/" + sheetname).convert())
    self.curr_sprite_sheet = self.sprite_sheets[0]

    self.image = pygame.Surface((self.width, self.height)).convert()
    self.image.blit(self.curr_sprite_sheet,
                      (0, 0),
                      (0, 0, self.width, self.height)
                    )
    self.image.set_colorkey(colors.BLACK)
    self.step_time = 0

  def update(self, elapsed, damage_maps):
    logging.debug('Update Character: {0}'.format(str(self)))
    if not self.alive:
      return

    self.move(elapsed)
    self.update_sprite(elapsed)
    self.apply_damage(elapsed, damage_maps)

    for skill in self.skills:
      skill.update(elapsed)

    self.attack.update(elapsed)

  def move(self, elapsed):
    if not self.moved:
      return

    x_pos = self.center[0]
    y_pos = self.center[1]

    x_move_dist = self.move_speed * elapsed
    y_move_dist = self.move_speed * elapsed
    x_dist = abs(x_pos - self.target_dest[0])
    y_dist = abs(y_pos - self.target_dest[1])

    if x_dist < x_move_dist:
      x_move_dist = x_dist
    if y_dist < y_move_dist:
      y_move_dist = y_dist

    if y_dist == 0 and x_dist == 0:
      self.step = 0
      self.step_time = 0.0

    if x_pos > self.target_dest[0]:
      x_pos -= x_move_dist
    elif x_pos < self.target_dest[0]:
      x_pos += x_move_dist

    if y_pos > self.target_dest[1]:
      y_pos -=  y_move_dist
    elif y_pos < self.target_dest[1]:
      y_pos += y_move_dist

    if not self.center[1] == y_pos:
      if self.center[1] > y_pos:
        self.orientation = 3
      else:
        self.orientation = 0
    if not self.center[0] == x_pos:
      if self.center[0] > x_pos:
        self.orientation = 1
      else:
        self.orientation = 2

    step = (x_pos, y_pos)
    grid_step = self.level.surf_to_grid(step)
    stepping_onto = self.level.grid[grid_step[0]][grid_step[1]]
    if stepping_onto in self.level.floor_tile_symbols:
      self.center = step
      if not self.location_grid_space == grid_step:
        self.location_grid_space = grid_step
        self.refresh_fov()
    '''
    else:
      x = self.center[0] - x_pos
      y = self.center[1] - y_pos

      self.center = (x_pos+x, y_pos+y)
      self.location_grid_space = self.level.surf_to_grid(step)
    '''

  def get_int_location(self):
    return tuple(map(int, self.center))

  def take_damage(self, damage):
    self.health_points -= damage
    if self.health_points <= 0:
      self.draw_color = self.dead_color
      self.image.blit(self.curr_sprite_sheet,
                    (0, 0),
                    (self.spritesheet_x, self.spritesheet_y, self.width, self.height)
                  )
      self.alive = False

  def draw(self, screen):
    if not self.alive:
      return

    x, y = self.center[0]-self.height/2, self.center[1]-self.width/2
    x = int(x)
    y = int(y)
    screen.blit(self.image, (x, y), (0, 0, self.width, self.height))
    if RUNTIME_LOG_LEVEL <= logging.DEBUG:
      pygame.draw.circle(screen, colors.GREEN, self.get_int_location(), 2)