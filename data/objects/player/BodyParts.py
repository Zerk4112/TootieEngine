import pymunk
import pygame
from pymunk import Vec2d

class CharacterPartCircle:
    def __init__(self, parent, color, offset, radius, friction):
        self.radius = radius
        self.offset = offset
        self.parent = parent
        self.color = color
        self.friction = friction
        self.shape = pymunk.Circle(self.parent.body, self.radius, self.offset)
        self.shape.filter = self.parent.torsoFilter
        self.shape.friction = friction


class CharacterPartSegment:
    def __init__(self, parent, color, offset, width, height, friction):
        self.offset = offset
        self.parent = parent
        self.color = color
        self.friction = friction
        self.width = width
        self.height = height
        self.vertices = [(-self.width, -self.height), (self.width, -self.height),
                         (self.width, self.height), (-self.width, self.height)]

        self.shape = pymunk.Segment(self.parent.body, (self.offset[0], self.offset[1]),
                                    (self.offset[0], self.offset[1] + self.height), self.width)
        self.shape.friction = friction


class CharacterPartSquare:
    def __init__(self, parent, color, offset, width, height, friction, vertices=None):
        self.offset = offset
        self.parent = parent
        self.color = color
        self.friction = friction
        self.width = width
        self.height = height
        if vertices is None:
            self.vertices = [(-self.width, -self.height), (self.width, -self.height),
                             (self.width, self.height), (-self.width, self.height)]
        else:
            self.vertices = vertices
        self.shape = pymunk.Poly(self.parent.body, self.vertices)
        self.shape.filter = self.parent.torsoFilter
        self.shape.friction = friction


class Arms:
    def __init__(self, parent, color, offset, joint_offset, bodytoJoint, friction, width, height, collide=True):
        self.offset = offset
        self.joint_offset = joint_offset
        self.bodytoJoint = bodytoJoint

        self.width = width
        self.height = height
        self.vertices = [(-self.width, -self.height), (self.width, -self.height),
                         (self.width, self.height), (-self.width, self.height)]
        self.parent = parent
        self.color = color
        self.friction = friction
        self.mass = 50
        self.moment = self.mass * 350
        self.body = pymunk.Body(self.mass, self.moment, body_type=pymunk.Body.DYNAMIC)
        self.body.position = (
            self.parent.body.position[0] + self.offset[0], self.parent.body.position[1] + self.offset[1])
        self.shape = pymunk.Poly(self.body, self.vertices)
        self.shape.filter = self.parent.armMask
        self.shape.friction = friction
        self.joint_pos = (self.bodytoJoint.position[0] + self.joint_offset[0],
                          self.bodytoJoint.position[1] + self.joint_offset[1])
        self.joint = pymunk.PivotJoint(self.body, self.bodytoJoint, self.joint_pos)
        self.joint.collide_bodies = collide


class Legs(Arms):
    def __init__(self, parent, color, offset, joint_offset, bodytoJoint, friction, width, height, mass, collide=True):
        super().__init__(parent, color, offset, joint_offset, bodytoJoint, friction, width, height)
        self.grounding = {
            'normal': Vec2d.zero(),
            'penetration': Vec2d.zero(),
            'impulse': Vec2d.zero(),
            'position': Vec2d.zero(),
            'body': None
        }
        self.well_grounded = False
        self.mass = mass
        self.moment = self.mass * 1600
        self.body = pymunk.Body(self.mass, self.moment, body_type=pymunk.Body.DYNAMIC)
        self.body.position = (
            self.parent.body.position[0] + self.offset[0], self.parent.body.position[1] + self.offset[1])
        self.shape = pymunk.Poly(self.body, self.vertices)
        self.shape.filter = self.parent.armMask
        self.shape.friction = friction
        self.joint_pos = (self.bodytoJoint.position[0] + self.joint_offset[0],
                          self.bodytoJoint.position[1] + self.joint_offset[1])
        self.joint = pymunk.PivotJoint(self.body, self.bodytoJoint, self.joint_pos)
        self.joint.collide_bodies = collide


class SpaceJoint:
    def __init__(self, space, parent, offsetBody):
        self.parent = parent
        self.offsetBody = offsetBody
        self.space = space
        self.body = pymunk.Body(999 * 99, pymunk.inf)
        self.body.position = (self.parent.body.position[0], self.parent.body.position[1] - 200)
        self.joint = pymunk.DampedSpring(self.body, self.parent.body, (0, 0), (0, 0), 50, 9800, 0)
        # self.joint.max_force = 999 ** 9
        self.jointed = False
        self.add_joint()
        self.joint_startTime = None

    def update_pos(self):
        self.body.position = (self.offsetBody.position[0], self.offsetBody.position[1] - 95)
        pass

    def remove_joint(self):
        if self.joint_startTime is not None:
            time_since_jointStart = pygame.time.get_ticks() - self.joint_startTime
            # print(time_since_jointStart)
            if time_since_jointStart > 100:
                if self.jointed:
                    self.space.remove(self.joint)
                    self.jointed = False

    def add_joint(self):
        self.joint_startTime = pygame.time.get_ticks()
        if self.jointed is False:
            self.space.add(self.joint)
            self.jointed = True


class RotationLimiter:
    def __init__(self, space, Body_A, Body_B, joint_offset, min, max, collide=True):
        self.space = space
        self.Body_A = Body_A
        self.Body_B = Body_B
        self.joint_offset = joint_offset
        self.min = min
        self.max = max
        self.joint_pos = (self.Body_B.position[0] + self.joint_offset[0],
                          self.Body_B.position[1] + self.joint_offset[1])
        self.joint = pymunk.RotaryLimitJoint(self.Body_A, self.Body_B, self.min, self.max)
        self.joint.collide_bodies = collide
        self.space.add(self.joint)
