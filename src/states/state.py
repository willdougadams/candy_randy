import pygame

class State:
  def __init__():
    self.update()
    self.draw()

  def update():
    raise NotImplementedError

  def draw():
    raise NotImplementedError

  def draw_loading_screen(self, progress, msg=[""]):
    w, h = self.screen.get_size()
    r = pygame.Rect(w/3, h/2, w/3, h/10)
    self.screen.fill((0, 0, 0))

    font_size = 15
    font_color = (255, 255, 255)

    self.font = pygame.font.SysFont("Courier", font_size)
    self.font_color = font_color

    for line_number, msg_str in enumerate(msg):
      label = self.font.render(msg_str, 1, font_color)
      self.screen.blit(label, (0, 0+line_number*font_size))

    pygame.draw.rect(self.screen, (255, 0, 255), [r.x, r.y, r.width, r.height], 3)
    pygame.draw.rect(self.screen, (255, 0, 255), [r.x, r.y, r.width*progress, r.height])
    pygame.display.flip()

