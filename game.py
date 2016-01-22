import pygame
from state import State
from pc import PC
from npc import NPC
from menu import Menu
from aoe import AOE

class Game(State):
    WHITE = (255, 255, 255)

    def __init__(self, screen):
        size = screen.get_size()
        self.highlighted_guy = 0
        self.active_skills = []
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.pcs = []
        self.npcs = []

        for p in range(3):
            self.pcs.append(PC((100, 100), 10, screen))

        for n in range(5):
            self.npcs.append(NPC((100 + n*100, 100 + n*20), 10, screen))

    def update(self, user_input, mouse_position):
        for event in user_input:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.manager.go_to(Menu(self.screen))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                self.highlighted_guy = (self.highlighted_guy + 1) % len(self.pcs)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.pcs[self.highlighted_guy].target_dest = mouse_position
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.active_skills.append(self.pcs[self.highlighted_guy].fire(mouse_position))

        self.active_skills = [a for a in self.active_skills if a is not None]
        self.active_skills = [a for a in self.active_skills if a.active_countdown > 0]

        for p in self.pcs:
            p.update()

        for n in self.npcs:
            n.update()

        for a in self.active_skills:
            a.update()

    def draw(self):
        self.screen.fill(self.WHITE)

        for a in self.active_skills:
            a.draw()

        for n in self.npcs:
            n.draw()

        for p in self.pcs:
            p.draw()

        pygame.display.flip()
