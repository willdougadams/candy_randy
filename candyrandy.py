'''
###
 Candy Randy Sweets Dealer Tycoon Game Simulator Saga
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
###
'''

import pygame
from game import Game
from state_manager import StateManager

HEIGHT = 1000
WIDTH = 1250
size = (WIDTH, HEIGHT)

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Candy Randy")
clock = pygame.time.Clock()

game = Game(screen)
mr_manager = StateManager(game) # We just say manager
done = False

while not done:
    clock.tick(61)

    user_input = pygame.event.get()
    mouse_position = pygame.mouse.get_pos()

    mr_manager.state.update(user_input, mouse_position)
    mr_manager.state.draw()

pygame.quit()
