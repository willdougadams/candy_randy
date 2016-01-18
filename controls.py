import pygame

class Controller:
    def __init__(self, controlled):
        self.player = controlled
        self.finish_condition = False

    def update(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_s]:
            self.player.accelerate(0, 5)

        if key[pygame.K_s]:
            self.player.accelerate(0, 5)
        elif key[pygame.K_w]:
            self.player.accelerate(0, -5)

        if key[pygame.K_d]:
            self.player.accelerate(5, 0)
        elif key[pygame.K_a]:
            self.player.accelerate(-5, 0)

        if key[pygame.K_ESCAPE]:
            self.finish_condition = True

    def done(self):
        return self.finish_condition
