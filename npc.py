from entity import Entity
from random import randint

class NPC(Entity):

    def update(self):
        seed = randint(1, 100)
        x_pos = self.center[0]
        y_pos = self.center[1]

        if seed == 1:
            x_pos += self.move_speed
        elif seed == 2:
            x_pos -= self.move_speed
        elif seed == 3:
            y_pos += self.move_speed
        elif seed == 4:
            y_pos -= self.move_speed

        self.center = (x_pos, y_pos)
