import pygame
from core import generate_level
import random
import threading
import math
import os
import logging

from states.state import State
from states.menu import Menu
from states.win_screen import WinScreen
from states.lose_screen import LoseScreen
from characters.pc import PC
from characters.npc import NPC
from skills.aoe import AOE
from core.hud import HUD
from core.level import Level
from items.item import Item


class Game(State):
  WHITE = (255, 255, 255)
  BLACK = (0, 0, 0)

  def __init__(self, screen, level=1, world=0):
    logging.info('Initializing Game...')
    self.ticks = 0
    self.screen = screen
    self.screen_w = self.screen.get_size()[0]
    self.screen_h = self.screen.get_size()[1]
    self.buffer_size = 16383 # <-- max size
    self.buffer_size = 16383 / 5
    self.buffer_frame = pygame.Surface((self.buffer_size, self.buffer_size))
    self.damage_maps = {}
    self.damage_maps['normal'] = pygame.Surface((self.buffer_size, self.buffer_size))
    self.damage_maps['tickleish'] = pygame.Surface((self.buffer_size, self.buffer_size))
    self.window_scale_factor = 2
    self.window_offset = (0, 0)
    self.pc_grid_location = (0, 0)
    self.current_level = level
    self.current_world = world
    self.pathfinding_index = 0

    self.active_pc = 0
    self.active_skills = []
    self.clock = pygame.time.Clock()

    self.pcs = []
    self.npcs = []
    self.items = []

    self.hud = HUD(self)
    self.level = Level(self.buffer_frame, self.current_level, self.current_world)
    gen_thread = threading.Thread(target=self.level.generate_grid)
    gen_thread.start()
    while not self.level.grid_generated:
      str_grid = [''.join(row) for row in self.level.grid]
      self.draw_loading_screen(self.level.get_progress(), msg=str_grid)
    self.level_w = self.level.get_w()
    self.level_h = self.level.get_h()

    spawn = generate_level.search_for_room(self.level.grid, start='center')
    spawn = self.level.grid_to_surf(spawn)
    self.items.append(Item('dagger.item', spawn))

    spots_taken = []
    for p in range(1):
      spawn = generate_level.search_for_room(self.level.grid, start='center')
      spots_taken.append(spawn)
      self.pcs.append(PC(tuple(map(lambda x: x*self.level.tile_size, spawn[::-1])), 10, self.buffer_frame, "res/pcs/Knight.pc", self.level))
    self.pc_grid_location = self.pcs[self.active_pc].location_grid_space
    self.level.regenerate_h_costs(self.pc_grid_location)

    npc_types = []
    npc_path = 'res/npcs/'
    for npc_file in os.listdir(npc_path):
      npc_types.append(npc_path+npc_file)

    for n in range(2):#len(npc_types)):
      spawn = generate_level.search_for_room(self.level.grid, start='random')
      while any(math.hypot(s[0]-spawn[0], s[1]-spawn[1]) < 20 for s in spots_taken):
        spawn = generate_level.search_for_room(self.level.grid, random.randint(1, len(self.level.grid)-2), random.randint(1, len(self.level.grid)-2))
      n = NPC(self.level.grid_to_surf(spawn), 10, self.buffer_frame, npc_types[n%len(npc_types)], self.level)
      new_path = self.level.get_path(n.get_int_location(), self.pcs[self.active_pc].get_int_location())
      n.add_path(new_path)
      self.npcs.append(n)

  def update(self, user_input, mouse_position, elapsed):
    self.ticks += 1
    self.handle_input(user_input, mouse_position)

    self.window_offset = get_new_offset(self)
    self.level.update(self.window_offset)
    self.active_skills = filter(lambda x: x is not None and x.alive, self.active_skills)

    if not self.pcs[self.active_pc].location_grid_space == self.pc_grid_location:
      self.level.regenerate_h_costs(self.pcs[self.active_pc].location_grid_space)
      self.pc_grid_location = self.pcs[self.active_pc].location_grid_space

    for _, surf in self.damage_maps.iteritems():
      surf.fill(Game.BLACK)

    for a in self.active_skills:
      a.update(elapsed)
      self.damage_maps = a.draw_damage(self.damage_maps)

    for n in self.npcs:
      n.update(elapsed, self.damage_maps)
      self.damage_maps = n.draw_damage_to_maps(self.damage_maps)

    path_timer = 25
    if (self.ticks+1)/path_timer > self.ticks/path_timer:
      n = self.npcs[self.pathfinding_index]
      new_path = self.level.get_path(n.get_int_location(), self.pcs[self.active_pc].get_int_location())
      n.add_path(new_path)
      self.pathfinding_index = (self.pathfinding_index+1)%len(self.npcs)

    for p in self.pcs:
      p.update(elapsed, self.damage_maps)

    # Win Condition
    if all(not n.alive for n in self.npcs):
      if self.current_level >= 1 or self.current_world >= 2:
        self.manager.go_to(WinScreen(self.screen, ("Congrats you win")))
      else:
        self.__init__(self.screen, self.current_level+1, self.current_world)

    # Lose condition
    if all(not p.alive for p in self.pcs):
      self.manager.go_to(LoseScreen(self.screen, ("Ur Ded, Try Again?", "Quit")))


  def draw(self):
    self.screen.fill(self.BLACK)
    self.buffer_frame.fill(self.BLACK)

    self.level.draw()

    for a in self.active_skills:
      a.draw(self.buffer_frame)

    for n in self.npcs:
      n.draw(self.buffer_frame)

    for p in self.pcs:
      self.level.highlight_tile(self.buffer_frame, p.center)
      p.draw(self.buffer_frame)

    for i in self.items:
      i.draw(self.buffer_frame)

    scale_factor = self.window_scale_factor
    w, h = self.screen.get_size()
    frame = pygame.Surface((w, h))
    frame.blit(self.buffer_frame, (0, 0), (self.level.offset[0], self.level.offset[1], w, h))
    frame = pygame.transform.scale(frame, (w*scale_factor, h*scale_factor))
    self.screen.blit(frame, (0, 0))

    self.hud.draw()

    pygame.display.flip()

  def handle_input(self, user_input, mouse_position):
    pressed = pygame.key.get_pressed()
    step_dist = 3
    up = pressed[pygame.K_w] * step_dist
    left = pressed[pygame.K_a] * step_dist
    down = pressed[pygame.K_s] * step_dist
    right = pressed[pygame.K_d] * step_dist

    if any([up, down, left, right]):
      now = self.pcs[self.active_pc].center
      later = (now[0]+right-left), (now[1]+down-up)
      self.pcs[self.active_pc].target_dest = later

    for event in user_input:
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.manager.go_to(Menu(self.screen, ('Quit', 'Main Menu', 'Resume Game')))
      elif event.type == pygame.MOUSEBUTTONDOWN:
        new_x = (mouse_position[0] / self.window_scale_factor + self.window_offset[0])
        new_y = (mouse_position[1] / self.window_scale_factor + self.window_offset[1])
        window_mouse_pos = (new_x, new_y)
        if event.button == 1:
          att = self.pcs[self.active_pc].fire_attack(window_mouse_pos)
          self.active_skills.append(att)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
          self.active_skills.append(self.pcs[self.active_pc].fire(window_mouse_pos))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
          skills_amt = len(self.pcs[self.active_pc].skills)
          self.pcs[self.active_pc].active_skill = (self.pcs[self.active_pc].active_skill + 1) % skills_amt
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
          skills_amt = len(self.pcs[self.active_pc].skills)
          self.pcs[self.active_pc].active_skill = (self.pcs[self.active_pc].active_skill - 1) % skills_amt

def get_new_offset(game):
    half_w = (game.screen_w/(2*game.window_scale_factor))
    half_h = (game.screen_h/(2*game.window_scale_factor))

    new_x = game.pcs[game.active_pc].center[0] - half_w
    new_y = game.pcs[game.active_pc].center[1] - half_h

    return (new_x, new_y)


