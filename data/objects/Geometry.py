import pygame
import pymunk

class KinematicBoundary:
    def __init__(self, point1_pos, point2_pos, width, color):
        self.point1 = point1_pos
        self.point2 = point2_pos
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.shape = pymunk.Segment(self.body, self.point1, self.point2, width)
        self.shape.friction = 0.99
        self.width = width
        self.color = color
        pass

    def addToSpace(self, space):
        space.add(self.shape)

    def draw(self, screen):
        pygame.draw.lines(screen, self.color, False, [ self.point1, self.point2 ], self.width)