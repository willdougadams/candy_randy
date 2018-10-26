import pygame
from states.state import State

class Menu(State):
  WHITE = (0, 255, 0)
  OTHER_COLOR = (255, 127, 255)

  def __init__(self, screen, items):
    self.screen = screen
    self.scr_width = self.screen.get_rect().width
    self.scr_height = self.screen.get_rect().height

    self.bg_color = self.WHITE
    self.clock = pygame.time.Clock()

    font_size = 30
    font_color = (255, 255, 255)

    self.items = items
    self.font = pygame.font.SysFont("Helvetica", font_size)
    self.font_color = font_color

    self.items = []
    self.button_rects = []
    self.highlighted_button = -1
    for index, item in enumerate(items):
      label = self.font.render(item, 1, font_color)

      width = label.get_rect().width
      height = label.get_rect().height

      posx = (self.scr_width / 2) - (width / 2)
      t_h = len(items) * height
      posy = (self.scr_height / 2) - (t_h / 2) + (index * height)

      self.items.append([item, label, (width, height), (posx, posy)])
      self.button_rects.append(pygame.Rect(posx, posy, width, height))

  def update(self, user_input, mouse_position, elapsed):
    self.highlighted_button = -1
    for i, button in enumerate(self.button_rects):
      if button.collidepoint(mouse_position):
        self.highlighted_button = i

    self.check_input(user_input)
    pygame.event.pump()


  def check_input(self, user_input):
    for event in user_input:
      if event.type == pygame.KEYDOWN: # key inputs
        if event.key == pygame.K_m:
          self.manager.go_back_state()
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if self.highlighted_button == 0:
          print "Exiting..."
          exit()
        if self.highlighted_button == 1:
          self.manager.go_back_state(2)
        if self.highlighted_button == 2:
          self.manager.go_back_state()

  def draw(self):
    self.screen.fill(self.WHITE)

    for i, (name, label, (width, height), (posx, posy)) in enumerate(self.items):
      self.screen.blit(label, (posx, posy))
      if i == self.highlighted_button:
        r = self.button_rects[i]
        pygame.draw.rect(self.screen, self.OTHER_COLOR, [r.x, r.y, r.width, r.height], 3)

    pygame.display.flip()
