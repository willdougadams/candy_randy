import pygame
from core import generate_level
import random
import threading
import math

from states.state import State
from states.menu import Menu
from characters.pc import PC
from characters.npc import NPC
from skills.aoe import AOE
from core.hud import HUD
from core.level import Level


class Game(State):
  WHITE = (255, 255, 255)
  BLACK = (0, 0, 0)

  def __init__(self, screen):
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

    self.active_pc = 0
    self.active_skills = []
    self.clock = pygame.time.Clock()

    self.pcs = []
    self.npcs = []

    self.hud = HUD(self)
    self.level = Level(self.buffer_frame)
    gen_thread = threading.Thread(target=self.level.generate_grid)
    gen_thread.start()
    while not self.level.grid_generated:
      str_grid = [''.join(row) for row in self.level.grid]
      self.draw_loading_screen(self.level.get_progress(), msg=str_grid)
    self.level_w = self.level.get_w()
    self.level_h = self.level.get_h()

    spots_taken = []
    for p in range(1):
      spawn = generate_level.search_for_room(self.level.grid, start='center')
      spots_taken.append(spawn)
      self.pcs.append(PC(tuple(map(lambda x: x*self.level.tile_size, spawn[::-1])), 10, self.buffer_frame, "res/pcs/Knight.pc", self.level))

    for n in range(3):
      spawn = generate_level.search_for_room(self.level.grid, start='random')
      while any(math.hypot(s[0]-spawn[0], s[1]-spawn[1]) < 20 for s in spots_taken):
        spawn = generate_level.search_for_room(self.level.grid, random.randint(1, len(self.level.grid)-2), random.randint(1, len(self.level.grid)-2))
      spots_taken.append(spawn)
      n = NPC(self.level.grid_to_surf(spawn), 10, self.buffer_frame, "res/npcs/slime.npc", self.level)
      new_path = self.level.get_path(n.get_int_location(), self.pcs[self.active_pc].get_int_location())
      n.add_path(new_path)
      self.npcs.append(n)

  def update(self, user_input, mouse_position, elapsed):
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
          self.manager.go_to(Menu(self.screen))
        elif event.key == pygame.K_TAB:
          self.active_pc = (self.active_pc + 1) % len(self.pcs)
        elif event.key == pygame.K_1:
          self.pcs[self.active_pc].active_skill = 0
        elif event.key == pygame.K_2:
          self.pcs[self.active_pc].active_skill = 1
        elif event.key == pygame.K_3:
          self.pcs[self.active_pc].active_skill = 2
      elif event.type == pygame.MOUSEBUTTONDOWN:
        new_x = (mouse_position[0] / self.window_scale_factor + self.window_offset[0])
        new_y = (mouse_position[1] / self.window_scale_factor + self.window_offset[1])
        window_mouse_pos = (new_x, new_y)
        if event.button == 1:
          self.active_skills.append(self.pcs[self.active_pc].fire_attack(window_mouse_pos))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
          self.active_skills.append(self.pcs[self.active_pc].fire(window_mouse_pos))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
          skills_amt = len(self.pcs[self.active_pc].skills)
          self.pcs[self.active_pc].active_skill = (self.pcs[self.active_pc].active_skill + 1) % skills_amt
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
          skills_amt = len(self.pcs[self.active_pc].skills)
          self.pcs[self.active_pc].active_skill = (self.pcs[self.active_pc].active_skill - 1) % skills_amt


    self.window_offset = get_new_offset(self)
    self.level.update(self.window_offset)
    self.active_skills = filter(lambda x: x is not None and x.alive, self.active_skills)

    for _, surf in self.damage_maps.iteritems():
      surf.fill(Game.BLACK)

    for a in self.active_skills:
      a.update(elapsed)
      self.damage_maps = a.draw_damage(self.damage_maps)

    for n in self.npcs:
      if len(n.path) < n.paths_original_length/2:
        new_path = self.level.get_path(n.get_int_location(), self.pcs[self.active_pc].get_int_location())
        n.add_path(new_path)
      n.update(elapsed, self.damage_maps)
      self.damage_maps = n.draw_damage_to_maps(self.damage_maps)

    for p in self.pcs:
      p.update(elapsed, self.damage_maps)

  def draw(self):
    self.screen.fill(self.BLACK)
    self.buffer_frame.fill(self.BLACK)

    self.level.draw()

    for a in self.active_skills:
      a.draw()

    for n in self.npcs:
      n.draw()

    for p in self.pcs:
      p.draw()

    scale_factor = self.window_scale_factor
    w, h = self.screen.get_size()
    frame = pygame.Surface((w, h))
    frame.blit(self.buffer_frame, (0, 0), (self.level.offset[0], self.level.offset[1], w, h))
    frame = pygame.transform.scale(frame, (w*scale_factor, h*scale_factor))
    self.screen.blit(frame, (0, 0))

    self.hud.draw()

    pygame.display.flip()

def get_new_offset(game):
    half_w = (game.screen_w/(2*game.window_scale_factor))
    half_h = (game.screen_h/(2*game.window_scale_factor))

    new_x = game.pcs[game.active_pc].center[0] - half_w
    new_y = game.pcs[game.active_pc].center[1] - half_h

    return (new_x, new_y)
