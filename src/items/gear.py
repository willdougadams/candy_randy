import logging

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
    swapped = self.items[item.gear_slot]
    self.items[item.gear_slot] = item
    return swapped

  def unequip(self, slot):
    item = self.items[slot]
    self.items[slot] = None
    return item

