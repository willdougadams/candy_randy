import logging

class Inventory:
  def __init__(self):
    logging.info('Initializing Inventory...')
    self.items = []
    self.capacity = 100

  def add_item(self, item):
    self.items.append(item)
    if sum([i.weight for i in self.items]) > self.capacity:
      logging.info('Can\'t add item, exceeded capacity.')
      _ = self.items.pop()
      return False

    logging.info('Added item to inventory...')
    return True

  def organize(self):
    self.items = sorted(self.items, key=lambda x: x.value)