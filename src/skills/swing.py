from skill import Skill

class Swing(Skill):

  def draw(self, screen, orientation):


  def draw_damage(self, damage_maps):
    for damage_type, surf in damage_maps.iteritems():
      center = (int(self.center[0]), int(self.center[1]))
      pygame.draw.circle(surf, self.current_color, center, int(self.r))

    return damage_maps

  def set_image(self, new_image):
    self.image = new_image
