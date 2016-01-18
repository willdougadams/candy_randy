from entity import Entity
from random import randint

class NPC(Entity):

    def update(self):
        seed = randint(1, 100)

        if seed == 1:
            self.accelerate(0, 5)
        elif seed == 2:
            self.accelerate(0, -5)
        elif seed == 3:
            self.accelerate(5, 0)
        elif seed == 4:
            self.accelerate(-5, 0)

        self.x += self.xs
        self.y += self.ys

        if self.xs > 0:
            self.xs -= 1
        elif self.xs < 0:
            self.xs += 1

        if self.ys > 0:
            self.ys -= 1
        elif self.ys < 0:
            self.ys += 1
