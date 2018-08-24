class State:
  def __init__():
    self.update()
    self.draw()

  def update():
    raise NotImplementedError

  def draw():
    raise NotImplementedError

  def draw_laoding_screen(self, progress):
    w, h = self.screen.get_height()
    r = pygame.Rect(w/3, h/2, w/3, h/10)
    self.screen.fill(0, 0, 0)
    pygame.draw.rect(self.screen, (255, 0, 255), [r.x, r.y, r.width, r.height], 3)
    pygame.draw.rect(self.screen, (255, 0, 255), [r.x, r.y, r.width, r.height])
    pygame.display.flip()

