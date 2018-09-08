import pygame # pylint: disable=E1121
from skills.aoe import AOE
from skills.bolt import Bolt
from skills.aura import Aura
from skills.attack import Attack

class PC():

  BLACK = (0, 0, 0)
  WHITE = (255, 255, 255)
  BLUE  = (0, 0, 255)
  GREEN = (0, 255, 0)
  RED = (255, 0, 0)

  MAX_HEALTH = 100
  STEP_LENGTH = 10

  def __init__(self, coord, r, buffer_frame, filename, level):
    self.attrib_dict = read_char_file(filename)
    w, h = pygame.display.get_surface().get_size()
    self.center = coord
    self.target_dest = coord
    self.screen = buffer_frame
    self.level = level
    self.orientation = 0
    self.step = 0
    self.location_grid_space = self.center[1]/len(self.level.grid), self.center[0]/len(self.level.grid[0])
    self.r = r
    self.width = int(self.attrib_dict["sprite_width"])
    self.height = int(self.attrib_dict["sprite_height"])
    self.spritesheet_x = 0
    self.spritesheet_y = 0

    self.alive_color = PC.BLUE
    self.dead_color = PC.BLACK
    self.draw_color = self.alive_color
    self.move_speed = int(self.attrib_dict['move_speed'])
    self.attack = Attack(self, self.screen, 'Attack.skill')
    self.max_speed = 15

    '''
    skills[] will hold the actual skill objects, and will refill skill
    slots appropriatly using skill_types, which is a list of the constructors
    '''
    self.skills = []
    self.skill_types = [AOE, Bolt, Aura]
    self.skill_files = ['AOE.skill', 'Bolt.skill', 'Aura.skill']
    for i, skill_type in enumerate(self.skill_types):
      self.skills.append(skill_type(self, self.screen, self.skill_files[i]))

    self.active_skill = 0
    self.health_points = int(self.attrib_dict["health"])
    self.alive = True

    self.sprite_sheets = []
    for sheetname in self.attrib_dict["spritesheets"]:
      self.sprite_sheets.append(pygame.image.load("res/DawnLike/" + sheetname).convert())
    self.curr_sprite_sheet = self.sprite_sheets[0]

    self.image = pygame.Surface((self.width, self.height)).convert()
    self.image.blit(self.curr_sprite_sheet,
                      (0, 0),
                      (0, 0, self.width, self.height)
                    )
    self.image.set_colorkey(PC.BLACK)
    self.step_time = 0

  def pc_update(self, elapsed, damage_maps):
    if not self.alive:
      return

    x_pos = self.center[0]
    y_pos = self.center[1]

    x_move_dist = self.move_speed * elapsed
    y_move_dist = self.move_speed * elapsed
    x_dist = abs(x_pos - self.target_dest[0])
    y_dist = abs(y_pos - self.target_dest[1])

    self.orientation = (0 if x_dist > 0 else 4)

    if x_dist < x_move_dist:
      x_move_dist = x_dist
    if y_dist < y_move_dist:
      y_move_dist = y_dist

    if x_pos > self.target_dest[0]:
      x_pos -= x_move_dist
    elif x_pos < self.target_dest[0]:
      x_pos += x_move_dist

    if y_pos > self.target_dest[1]:
      y_pos -=  y_move_dist
    elif y_pos < self.target_dest[1]:
      y_pos += y_move_dist

    step = (x_pos, y_pos)
    grid_step = int(step[1]/self.level.tile_size), int(step[0]/self.level.tile_size)

    stepping_onto = self.level.grid[grid_step[0]][grid_step[1]]
    if stepping_onto in self.level.floor_tile_symbols:
      self.center = step
      self.location_grid_space = grid_step
  
    self.step_time += elapsed
    if self.step_time > 0.5:
      self.step = (self.step + 1) % 4
      self.step_time = 0.0

    self.image.blit(self.curr_sprite_sheet, (0, 0), (self.step * 16, self.orientation * 16, 16, 16))
    self.image.set_colorkey(PC.BLACK)
    self.rect = self.image.get_rect()

    for skill in self.skills:
      skill.update(elapsed)
    
    self.apply_damage(damage_maps, elapsed)

  def draw(self):
    x, y = self.center
    x = int(x)
    y = int(y)

    if self.alive:
      self.screen.blit(self.image, (x - self.width/2, y - self.height/2), (0, 0, self.width, self.height))

  '''
  PC.fire() calls the Skill.fire() method of the currently selected skill,
  which will return the fired skill object if the skill is available, otherwise
  returns None.

  If the skill can be fired, the skill object will be returned to
  Game.active_skills[], and a new Skill object will be created and put in the PC's
  skills[].  Game.active_skills[] ignores None entries, and continues
  handling active Skills.
  '''
  def fire(self, coord):
    ret_skill = self.skills[self.active_skill].fire(coord)
    if ret_skill is not None:
      config_file = self.skill_files[self.active_skill]
      self.skills[self.active_skill] = self.skill_types[self.active_skill](self, self.screen, config_file)
    return ret_skill

  def fire_attack(self, coord):
    attack = self.attack.fire(coord)
    if attack is not None:
      self.attack = Attack(self, self.screen, self.attack_file)
    return attack

  def apply_damage(self, damage_maps, elapsed):
    # pcs take damage with green and do damage with red
    for damage_type, surf in damage_maps.iteritems():
      damage_done = surf.get_at(tuple(map(int, self.center))).g
      print damage_done
      self.take_damage(damage_done*elapsed)

  def take_damage(self, damage):
    self.health_points -= damage
    if self.health_points <= 0:
      self.draw_color = self.dead_color
      self.image.blit(self.curr_sprite_sheet,
                    (0, 0),
                    (self.spritesheet_x, self.spritesheet_y, self.width, self.height)
                  )
      self.alive = False


def read_char_file(filename):
  attribute_dict = {}
  with open(filename) as fin:
    lines = fin.readlines()

  for line in lines:
    if (not line.strip()) or line[0] == "#":
      continue

    attribute = line.split(":")[0]
    value = line.split(":")[1]
    attribute_dict[attribute] = (value if len(value.split()) == 1 else value.split())
    if len(attribute_dict[attribute]) == 1:
      attribute_dict[attribute] = attribute_dict[attribute][0]

  return attribute_dict
