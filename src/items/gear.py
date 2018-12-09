import pygame
import logging

from core.util import colors

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
    if self.items['left_hand'] is None:
      fist = pygame.Surface((20, 10))
      fist.fill(colors.BLUE)
      return fist
    else:
      img = self.items['left_hand'].image
      img = pygame.transform.rotate(img, 315)
      w, h = img.get_size()
      full_surface = pygame.Surface((w, h)).convert()
      full_surface.blit(img, (0, 0))
      if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
        pygame.draw.rect(full_surface, colors.PINK, (0, 0, full_surface.get_width()-1, full_surface.get_height()-1), 1)
      full_surface.set_colorkey(colors.BLACK)
      return full_surface