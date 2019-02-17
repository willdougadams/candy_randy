'''
###
 Candy Randy Sweets Dealer Tycoon Game Simulator Saga
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
###
'''

import logging
import pygame
import time
import sys
from states.main_menu import MainMenu
from states.state_manager import StateManager

log_format = '%(levelname)s %(asctime)s - %(message)s'
log_level = logging.INFO
if '--debug' in sys.argv:
  log_level = logging.DEBUG
logging.basicConfig(filename='log.txt', level=log_level, format=log_format, filemode='w')

logging.info('Initializing pygame...')
pygame.init()

WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
WIDTH = 1280 # int(HEIGHT * 0.80)
HEIGHT = 800 # int(WIDTH * 0.80)
size = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Dungeon Crawler - The Game")
clock = pygame.time.Clock()

main_menu = MainMenu(screen)
mr_manager = StateManager(main_menu) # We just say manager
done = False

def main():
  start = time.time()
  time.sleep(0.001)
  end = time.time()
  while not done:
    elapsed = end - start
    start = time.time()
    user_input = pygame.event.get()
    mouse_position = pygame.mouse.get_pos()

    try:
      mr_manager.state.update(user_input, mouse_position, elapsed)
      mr_manager.state.draw()
    except Exception as e:
      logging.critical(e)
      exit()
    end = time.time()
  pygame.quit()


if __name__ == '__main__':
  main()
