'''
###
 Candy Randy Sweets Dealer Tycoon Game Simulator Saga
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
###
'''

import pygame
from time import sleep
from entity import Entity
from npc import NPC
# from controls import Controller
from state_manager import StateManager
from game import Game

pygame.init()

WHITE = (255, 255, 255)
HEIGHT = 800
WIDTH = 1000
size = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Candy Randy")

game = Game(screen)
mr_manager = StateManager(game)

done = False

while not done:
    sleep(.01)

    user_input = pygame.event.get()
    mouse_position = pygame.mouse.get_pos()
    mr_manager.state.update(user_input, mouse_position)
    mr_manager.state.draw()

    for event in user_input:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

pygame.quit()
