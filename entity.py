import pygame
from aoe import AOE

class Entity:

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE  = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    def __init__(self, coord, r, screen):
        self.target_dest = (0, 0)
        self.screen = screen
        self.center = coord
        self.r = r
        self.draw_color = Entity.BLACK
        self.move_speed = 3
        self.max_speed = 15

        self.skills = []
        self.skills.append(AOE(50, self.screen))
        self.active_skill = 0

    def update(self):
        x_pos = self.center[0]
        y_pos = self.center[1]

        x_move_dist = self.move_speed
        y_move_dist = self.move_speed
        x_dist = abs(x_pos - self.target_dest[0])
        y_dist = abs(y_pos - self.target_dest[1])

        if x_dist < x_move_dist:
            x_move_dist = x_dist
        if y_dist < y_move_dist:
            y_move_dist = y_dist

        if x_pos > self.target_dest[0]:
            x_pos -= x_move_dist
        elif x_pos < self.target_dest[0]:
            x_pos += x_move_dist

        if y_pos > self.target_dest[1]:
            y_pos -=  y_move_dist
        elif y_pos < self.target_dest[1]:
            y_pos += y_move_dist

        self.center = (x_pos, y_pos)

        for i, skill in enumerate(self.skills):
            skill.update()

    def draw(self):
        pygame.draw.circle(self.screen, self.draw_color, self.center, self.r, 2)

    def fire(self, coord):
        ret_skill = self.skills[self.active_skill].fire(coord)
        self.skills[self.active_skill] = AOE(50, self.screen)
        return ret_skill
