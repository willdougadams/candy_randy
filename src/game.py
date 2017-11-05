import pygame
from state import State
from pc import PC
from npc import NPC
from menu import Menu
from aoe import AOE
from hud import HUD

class Game(State):
  WHITE = (255, 255, 255)

  def __init__(self, screen):
    self.screen = screen

    size = self.screen.get_size()
    self.background = pygame.Surface(self.screen.get_size())
    self.background = self.background.convert()

    screen.blit(self.background, (0,0))

    self.active_pc = 0
    self.active_skills = []
    self.clock = pygame.time.Clock()

    self.pcs = []
    self.npcs = []

    self.hud = HUD(self)

    for p in range(3):
      self.pcs.append(PC((100, 100), 10, screen, "res/pcs/Knight.pc"))

    for n in range(5):
      self.npcs.append(NPC((100 + n*100, 100 + n*20), 10, screen, "res/npcs/beholder.npc"))

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
        if event.button == 1:
          self.pcs[self.active_pc].target_dest = mouse_position
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
          self.active_skills.append(self.pcs[self.active_pc].fire(mouse_position))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
          skills_amt = len(self.pcs[self.active_pc].skills)
          self.pcs[self.active_pc].active_skill = (self.pcs[self.active_pc].active_skill + 1) % skills_amt
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
          skills_amt = len(self.pcs[self.active_pc].skills)
          self.pcs[self.active_pc].active_skill = (self.pcs[self.active_pc].active_skill - 1) % skills_amt

    self.active_skills = [a for a in self.active_skills if a is not None]
    self.active_skills = [a for a in self.active_skills if a.active_countdown > 0]

    for p in self.pcs:
      p.pc_update(elapsed)

    for n in self.npcs:
      n.npc_update(elapsed)

    '''
    Pass updated pcs and npcs to each skill to check for collisions.
    '''
    for a in self.active_skills:
      a.update(self.pcs, self.npcs, elapsed)

  def draw(self):
    self.screen.fill(self.WHITE)

    for a in self.active_skills:
      a.draw()

    for n in self.npcs:
      n.draw()

    for p in self.pcs:
      p.draw()

    self.hud.draw()

    pygame.display.flip()