import pygame
from state import State
from entity import Entity
from controls import Controller
from npc import NPC
from menu import Menu

class Game(State):
    WHITE = (255, 255, 255)

    def __init__(self, screen):
        size = screen.get_size()
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.player = Entity(size[0]/2, size[1]/2, 3, 3, 10, 10, screen)
        self.controls = Controller(self.player)
        self.baddies = []

        for i in xrange(10):
            temp_baddie = NPC(size[0]/2, size[1]/2, 3, 3, 10, 10, screen)
            self.baddies.append(temp_baddie)

    def update(self):
        self.controls.update();
        self.player.update()

        for bad in self.baddies:
            bad.update()

        if pygame.key.get_pressed()[pygame.K_e]:
            self.manager.go_to(Menu(self.screen))

        pygame.event.pump()

    def draw(self):
        self.screen.fill(self.WHITE)

        self.player.draw()
        for bad in self.baddies:
            bad.draw()

        pygame.display.flip()
