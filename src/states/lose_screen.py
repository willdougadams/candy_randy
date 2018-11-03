import pygame
import logging
from states.menu import Menu

class LoseScreen(Menu):
  def __init__(self, screen, items):
      Menu.__init__(self, screen, items)
  def check_input(self, user_input):
      for event in user_input:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
          if self.highlighted_button == 0:
            self.manager.go_back_state(2)
          if self.highlighted_button == 1:
            logging.info("User lost, quit from deadscreen")
            exit()


