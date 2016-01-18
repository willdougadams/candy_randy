import pygame

class Entity:

    BLACK    = (   0,   0,   0)
    WHITE    = ( 255, 255, 255)
    BLUE     = (   0,   0, 255)
    GREEN    = (   0, 255,   0)
    RED      = ( 255,   0,   0)
    PI = 3.141592653

    def __init__(self, x, y, xs, ys, w, h, screen):
        self.screen = screen
        self.x = x
        self.y = y
        self.xs = xs
        self.ys = ys
        self.w = w
        self.h = h
        self.max_speed = 15

    def __del__(self):
        pass

    def update(self):
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
