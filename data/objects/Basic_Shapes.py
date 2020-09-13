import pymunk
import pygame


class LabObject:
    def __init__(self, pos, space, mass, friction, moment, color):
        self.space = space
        self.color = color
        self.mass = mass
        self.moment = moment
        self.body = pymunk.Body(self.mass, self.moment, body_type=pymunk.Body.DYNAMIC)
        self.friction = friction
        self.body.position = pos

    def addToSpace(self):
        self.space.add(self.body, self.shape)


class Ball(LabObject):
    def __init__(self, pos, space, mass, friction, moment, color, radius):
        super().__init__(pos, space, mass, friction, moment, color)
        self.radius = radius
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.friction = self.friction


class Square(LabObject):
    def __init__(self, pos, space, mass, friction, moment, color, vertices):
        super().__init__(pos, space, mass, friction, moment, color)
        self.shape = pymunk.Poly(self.body, vertices)
        self.shape.friction = self.friction
