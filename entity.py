import pygame

class Entity:

    BLACK    = (   0,   0,   0)
    WHITE    = ( 255, 255, 255)
    BLUE     = (   0,   0, 255)
    GREEN    = (   0, 255,   0)
    RED      = ( 255,   0,   0)
    PI = 3.141592653

    def __init__(self, x, y, xs, ys, w, h, screen):
        self.target_dest = (50, 50)
        self.screen = screen
        self.x = x
        self.y = y
        self.xs = xs
        self.ys = ys
        self.w = w
        self.h = h
        self.rectangle = pygame.Rect(x, y, w, h)
        self.max_speed = 15

    def __del__(self):
        pass

    def update(self):
        x_move_dist = 3
        y_move_dist = 3
        x_dist = abs(self.x - self.target_dest[0])
        y_dist = abs(self.y - self.target_dest[1])

        if x_dist < x_move_dist:
            x_move_dist = x_dist

        if y_dist < y_move_dist:
            y_move_dist = y_dist

        if self.x > self.target_dest[0]:
            self.x -= x_move_dist
        elif self.x < self.target_dest[0]:
            self.x += x_move_dist

        if self.y > self.target_dest[1]:
            self.y -= y_move_dist
        elif self.y < self.target_dest[1]:
            self.y += y_move_dist

        if self.rectangle.collidepoint(self.target_dest):
            self.xs = 0
            self.ys = 0

    def accelerate(self, xs, ys):
        self.xs += xs
        self.ys += ys

        if self.ys > self.max_speed:
            self.ys = self.max_speed
        if self.xs > self.max_speed:
            self.xs = self.max_speed
        if self.xs < -self.max_speed:
            self.xs = -self.max_speed
        if self.ys < -self.max_speed:
            self.ys = -self.max_speed

    def draw(self):
        pygame.draw.rect(self.screen, Entity.BLACK, [self.x, self.y, self.h, self.w], 2)
