import pygame
import logging
from skills.aoe import AOE
from skills.bolt import Bolt
from skills.aura import Aura
from skills.jab import Jab
from items.inventory import Inventory
from items.gear import Gear
from characters.character import Character

from core.util import read_config, colors, RUNTIME_LOG_LEVEL

class PC(Character):

  MAX_HEALTH = 100
  STEP_LENGTH = 10

  def __init__(self, coord, r, buffer_frame, filename, level):
    Character.__init__(self, coord, r, buffer_frame, filename, level)

  def update(self, elapsed, damage_maps):
    logging.debug('Update Character: {0}'.format(str(self)))
    
    if not self.alive:
      return
    Character.update(self, elapsed, damage_maps)

  def move(self, elapsed):
    Character.move(self, elapsed)
    self.level.regenerate_h_costs(self.level.surf_to_grid(self.center))

  def update_sprite(self, elapsed):
    self.step_time += elapsed
    if self.step_time > 0.25:
      self.step = (self.step + 1) % 4
      self.step_time = 0.0

    self.image.blit(self.curr_sprite_sheet, (0, 0), (self.step * 16, self.orientation * 16, 16, 16))
    self.image.set_colorkey(colors.BLACK)
    self.rect = self.image.get_rect()

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
      self.skills[self.active_skill] = self.skill_types[self.active_skill](self, config_file)
    return ret_skill

  def fire_attack(self, coord):
    dps = self.gear.get_dps()
    attack = self.attack.fire(coord, dps)
    
    if attack is not None:
      self.set_attack(self.gear.get_attack(self))

    return attack

  def set_attack(self, attack):
    self.attack = attack
    self.attack.set_image(self.gear.get_attack_image())

  def apply_damage(self, elapsed, damage_maps):
    # pcs take damage with green and do damage with red
    for damage_type, surf in damage_maps.iteritems():
      damage_done = surf.get_at(self.get_int_location()).g
      damage_done *= elapsed
      self.take_damage(damage_done)

  def pick_up(self, item):
    if item.equip_slot == 'hand':
      item.equip_slot = 'right_hand'

    if self.gear.items[item.equip_slot] is None:
      self.gear.equip(item)
      self.attack = self.gear.get_attack(self)
    else:
      self.inventory.add_item(item)

  def refresh_fov(self):
    self.visible_tiles = self.level.get_fov(self.location_grid_space, self.orientation)

