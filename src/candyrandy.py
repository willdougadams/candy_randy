'''
###
 Candy Randy Sweets Dealer Tycoon Game Simulator Saga
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
###
'''

import pygame
import time
from states.game import Game
from states.state_manager import StateManager

pygame.init()

WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
WIDTH = 1280 # int(HEIGHT * 0.80)
HEIGHT = 800 # int(WIDTH * 0.80)
size = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Candy Randy")
clock = pygame.time.Clock()

game = Game(screen)
mr_manager = StateManager(game) # We just say manager
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

    mr_manager.state.update(user_input, mouse_position, elapsed)
    mr_manager.state.draw()

    end = time.time()
  pygame.quit()


if __name__ == '__main__':
  main()
