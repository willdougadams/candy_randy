import src.level
import time
import pygame

pygame.init()
WIDTH = 1280 # int(HEIGHT * 0.80)
HEIGHT = 800 # int(WIDTH * 0.80)
size = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Map Viewer")

level = src.level.Level(screen)

while True:
  screen.fill((255, 255, 255))
  level.draw()
  pygame.display.flip()

  time.sleep(1)
