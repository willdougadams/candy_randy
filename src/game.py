import pygame
from state import State
from pc import PC
from npc import NPC
from menu import Menu
from aoe import AOE
from hud import HUD
from level import Level

class Game(State):
  WHITE = (255, 255, 255)

  def __init__(self, screen):
    self.screen = screen
    self.screen_w = self.screen.get_size()[0]
    self.screen_h = self.screen.get_size()[1]
    self.buffer_size = 16383 # <-- max size
    self.buffer_size = 16383 / 5
    self.buffer_frame = pygame.Surface((self.buffer_size, self.buffer_size))

    self.active_pc = 0
    self.active_skills = []
    self.clock = pygame.time.Clock()

    self.pcs = []
    self.npcs = []

    self.hud = HUD(self)
    self.level = Level(self.buffer_frame)
    self.level_w = self.level.get_w()
    self.level_h = self.level.get_h()

    for p in range(1):
      self.pcs.append(PC((100, 100), 10, self.buffer_frame, "res/pcs/Knight.pc"))

    for n in range(5):
      self.npcs.append(NPC((100 + n*100, 100 + n*100), 10, self.buffer_frame, "res/npcs/beholder.npc"))

    self.window_scale_factor = 2
    self.window_offset = (0, 0)

  def update(self, user_input, mouse_position, elapsed):
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
          self.pcs[self.active_pc].target_dest = window_mouse_pos
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

    self.active_skills = [a for a in self.active_skills if a is not None]
    self.active_skills = [a for a in self.active_skills if a.active_countdown > 0]

    for p in self.pcs:
      p.pc_update(elapsed)

    for n in self.npcs:
      n.npc_update(elapsed)

    for a in self.active_skills:
      a.update(self.pcs, self.npcs, elapsed)

  def draw(self):
    self.screen.fill(self.WHITE)
    self.buffer_frame.fill(self.WHITE)

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

    max_x = game.level_w/game.window_scale_factor - half_w
    max_y = game.level_h/game.window_scale_factor - half_h

    '''
    if new_x < 0:
        new_x = 0
    elif new_x > max_x:
        new_x = max_x

    if new_y < 0:
        new_y = 0
    elif new_y > max_y:
        new_y = max_y
    '''

    return (new_x, new_y)
