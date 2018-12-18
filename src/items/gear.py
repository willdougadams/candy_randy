import pygame
import logging

from skills.jab import Jab
from skills.swing import Swing

from core.util import colors, trim_image

class Gear:
  def __init__(self):
    self.items = {
      'head': None,
      'feet': None,
      'right_hand': None,
      'left_hand': None,
      'torso': None,
      'belt': None,
      'potion1': None,
      'potion2': None
    }

  def equip(self, item):
    """
    Takes an item and assigns it to its gearslot,
    returning the item it replaces, if any
    """
    swapped = self.items[item.equip_slot]
    self.items[item.equip_slot] = item
    return swapped

  def unequip(self, slot):
    item = self.items[slot]
    self.items[slot] = None
    return item

  def get_reach(self):
    left = 25
    if self.items['left_hand'] is not None:
      left = self.items['left_hand'].length

    return left

  def get_attack_image(self):
    if self.items['right_hand'] is None:
      fist = pygame.Surface((20, 10))
      fist.fill(colors.BLUE)
      return fist
    else:
      img = self.items['right_hand'].image
      img = pygame.transform.rotate(img, 315)
      img = trim_image(img)
      img.set_colorkey(colors.BLACK)
      if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
        pygame.draw.rect(img, colors.PINK, (0, 0, img.get_width()-1, img.get_height()-1), 2)
      return img

  def get_attack(self, caster):
    item = self.items['right_hand']
    if item == None:
      return Jab(caster, 'Swing.skill', self.get_reach())

    t = item.get_attack_type()
    if t == 'jab':
      return Jab(caster, item.attack_file, self.get_reach())
    else:
      return Attack(caster, item.attack_file, self.get_reach())
