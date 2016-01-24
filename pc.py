import pygame
from aoe import AOE
from bolt import Bolt

class PC:

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE  = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    MAX_HEALTH = 100

    def __init__(self, coord, r, screen):
        self.target_dest = (0, 0)
        self.screen = screen
        self.center = coord
        self.r = r

        self.alive_color = PC.BLUE
        self.dead_color = PC.BLACK
        self.draw_color = self.alive_color
        self.move_speed = 3
        self.max_speed = 15

        '''
        skills[] will hold the actual skill objects, and will refill skill
        slots appropriatly using skill_types, which is a list of the constructors
        '''
        self.skills = []
        self.skill_types = []
        self.skill_types.append(AOE)
        self.skill_types.append(Bolt)
        for skill_type in self.skill_types:
            self.skills.append(skill_type(self, self.screen))

        self.active_skill = 0
        self.health_points = PC.MAX_HEALTH
        self.alive = True

    def update(self):
        if not self.alive:
            return

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

        for skill in self.skills:
            skill.update([], [])

    def draw(self):
        pygame.draw.circle(self.screen, self.draw_color, self.center, self.r, 2)

    '''
    PC.fire() calls the Skill.fire() method of the currently selected skill,
    which will return the fired skill object if the skill is available, otherwise
    returns None.

    If the skill can be fired, the skill object will be returned to
    Game.active_skills[], and a new Skill object will be created and put in the PC's
    skills[].  Game.active_skills[] ignores None entries, and continues
    handling active Skills.
    '''
    def fire(self, coord):
        ret_skill = self.skills[self.active_skill].fire(coord)
        if ret_skill is not None:
            self.skills[self.active_skill] = self.skill_types[self.active_skill](self, self.screen)
        return ret_skill

    def take_damage(self, damage):
        if self.health_points <= 0:
            self.draw_color = self.dead_color
            self.alive = False
        else:
            self.health_points -= damage
