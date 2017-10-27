from pc import PC
from random import randint

class NPC(PC):
    def __init__(self, coord, r, screen):
        PC.__init__(self, coord, r, screen)
        self.target_dest = (0, 0)
        self.screen = screen
        self.center = coord
        self.r = r
        self.move_speed = 3
        self.max_speed = 15

        self.alive_color = PC.RED
        self.dead_color = PC.BLACK
        self.draw_color = self.alive_color

        self.health_points = PC.MAX_HEALTH
        self.alive = True

    def update(self):
        if not self.alive:
            return

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
