import pygame
from state import State
from entity import Entity
from npc import NPC
from menu import Menu

class Game(State):
    WHITE = (255, 255, 255)

    def __init__(self, screen):
        size = screen.get_size()
        self.highlighted_guy = 0
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.pc = []
        self.pc_rects = []
        for p in range(3):
            self.pc.append(Entity(size[0]/2, size[1]/2, 3, 3, 10, 10, screen))
            self.pc_rects.append(self.pc[-1])
        # self.controls = Controller(self.player)
        self.baddies = []

        for i in xrange(10):
            temp_baddie = NPC(size[0]/2, size[1]/2, 3, 3, 10, 10, screen)
            self.baddies.append(temp_baddie)

    def update(self, user_input, mouse_position):
        for event in user_input:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                self.manager.go_to(Menu(self.screen))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                self.highlighted_guy = (self.highlighted_guy + 1) % len(self.pc)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.pc[self.highlighted_guy].target_dest = mouse_position

        for p in self.pc:
            p.update()

        for bad in self.baddies:
            bad.update()

    def draw(self):
        self.screen.fill(self.WHITE)

        for p in self.pc:
            p.draw()
        for bad in self.baddies:
            bad.draw()

        pygame.display.flip()
