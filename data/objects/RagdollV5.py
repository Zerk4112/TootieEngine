import pymunk
import random
import pygame
from pygame.locals import *

default_body_friction = 0.99
default_moment_multiplier = 150


class SpaceJoint:
    def __init__(self, space, parent, offsetBody):
        self.parent = parent
        self.offsetBody = offsetBody
        self.space = space
        self.body = pymunk.Body(999 * 99, pymunk.inf)
        self.body.position = (self.parent.body.position[0], self.parent.body.position[1] - 100)
        self.joint = pymunk.DampedSpring(self.body, self.parent.body, (0, 0), (0, 0), 10, 9800, 0)
        # self.joint.max_force = 999 ** 9

        self.add_joint()

    def update_pos(self):
        self.body.position = (self.offsetBody.body.position[0], self.offsetBody.body.position[1] - 140)
        pass

    def remove_joint(self):
        self.space.remove(self.joint)

    def add_joint(self):
        self.space.add(self.joint)

class RagdollV4:
    def __init__(self, space, pos):
        self.space = space
        self.armMask = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b1, categories=0b1)
        self.legMask = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b1, categories=0b1)
        self.torsoFilter = pymunk.ShapeFilter(categories=0b1)
        self.origin_point = pos

        self.upperTorso = UpperTorso(self, (0, 0), 200, 40, 60)
        self.lowerTorso = LowerTorso(self, (0, 25), 100, 60, 25, (0, 16), self.upperTorso.body)
        self.leftUpperArm = Arm(self, (-38, -23), 75, 35, 15, (-25, -23), self.upperTorso.body, False)
        self.leftForeArm = Arm(self, (-77, -23), 50, 35, 15, (-20, -0), self.leftUpperArm.body)
        self.rightUpperArm = Arm(self, (38, -23), 75, 35, 15, (25, -23), self.upperTorso.body, False)
        self.rightForeArm = Arm(self, (77, -23), 50, 35, 15, (20, -0), self.rightUpperArm.body)

        self.leftThigh = Leg(self, (-12, 58), 75, 15, 35, (-11, 12), self.lowerTorso.body, False)
        self.leftCalf = Leg(self, (-12, 93), 50, 15, 35, (0, 12), self.leftThigh.body, False)

        self.rightThigh = Leg(self, (12, 58), 75, 15, 35, (11, 12), self.lowerTorso.body, False)
        self.rightCalf = Leg(self, (12, 93), 50, 15, 35, (0, 12), self.rightThigh.body, False)

        self.head = Head(self, (0, -45), 200, 40, 60, (0, -30), self.upperTorso.body)
        # self.standing_joint = SpaceJoint(self.space, self.head, self.lowerTorso)
        self.standing = True


    # def toggle_Standing(self):
    #
    #     self.standing = not self.standing
    #
    #     if self.standing:
    #         self.standing_joint.add_joint()
    #     else:
    #         self.standing_joint.remove_joint()
    def on_event(self, event):
        if event.type == KEYDOWN and event.key == K_LEFT:
            # self.upperTorso.body.apply_force_at_world_point((-500 * 9999, 0), self.upperTorso.body.position)
            print("walking left")

        # if event.type == KEYDOWN and event.key == K_h:
        #     self.toggle_Standing()

    def addToSpace(self):
        self.upperTorso.addToSpace()
        self.lowerTorso.addToSpace()
        self.leftUpperArm.addToSpace()
        self.leftForeArm.addToSpace()
        self.rightUpperArm.addToSpace()
        self.rightForeArm.addToSpace()
        self.leftThigh.addToSpace()
        self.leftCalf.addToSpace()
        self.rightThigh.addToSpace()
        self.rightCalf.addToSpace()
        self.head.addToSpace()


class StandingJoint():
    def __init__(self, parent):
        pass


class BodyPart:
    def __init__(self, parent, offset, mass, width, height):
        self.offset = offset
        self.parent = parent
        self.space = self.parent.space
        self.vertices = [(-width / 2, -height / 2),
                         (width / 2, -height / 2),
                         (width / 2, height / 2),
                         (-width / 2, height / 2)]
        self.friction = default_body_friction
        self.body = pymunk.Body(mass, mass * default_moment_multiplier, body_type=pymunk.Body.DYNAMIC)
        self.body.position = (self.parent.origin_point[0] + offset[0], self.parent.origin_point[1] + offset[1])

    def addToSpace(self):
        self.space.add(self.body, self.shape)

    def setShape(self):
        self.shape = pymunk.Poly(self.body, self.vertices)
        self.shape.friction = default_body_friction


class BodyPart_WithJoint(BodyPart):
    def __init__(self, parent, offset, mass, width, height, jointOffset, bodytoJoint, collide=True):
        super().__init__(parent, offset, mass, width, height)
        self.joint_offset = jointOffset
        self.bodytoJoint = bodytoJoint
        self.joint_pos = (self.bodytoJoint.position[0] + self.joint_offset[0],
                          self.bodytoJoint.position[1] + self.joint_offset[1])
        self.joint = pymunk.PivotJoint(self.body, self.bodytoJoint, self.joint_pos)
        self.joint.collide_bodies = collide
        self.space.add(self.joint)


class Head(BodyPart_WithJoint):
    def __init__(self, parent, offset, mass, width, height, jointOffset, bodytoJoint, collide=True):
        super().__init__(parent, offset, mass, width, height, jointOffset, bodytoJoint, collide)
        self.setShape()

    def setShape(self):
        self.shape = pymunk.Circle(self.body, 15)
        self.shape.friction = default_body_friction


class UpperTorso(BodyPart):
    def __init__(self, parent, offset, mass, width, height):
        super().__init__(parent, offset, mass, width, height)
        self.vertices = [(-width / 2, -height / 2), (width / 2, -height / 2),
                         (width / 3, height / 4), (-width / 3, height / 4)]
        self.setShape()
        self.shape.filter = self.parent.torsoFilter



class LowerTorso(BodyPart_WithJoint):
    def __init__(self, parent, offset, mass, width, height, jointOffset, bodytoJoint, collide=True):
        super().__init__(parent, offset, mass, width, height, jointOffset, bodytoJoint, collide)
        self.vertices = [(-width / 4, -height / 4),
                         (width / 4, -height / 4),
                         (width / 3, height / 2),
                         (-width / 3, height / 2)]
        self.setShape()
        self.shape.filter = self.parent.torsoFilter


class Arm(BodyPart_WithJoint):
    def __init__(self, parent, offset, mass, width, height, jointOffset, bodytoJoint, collide=True):
        super().__init__(parent, offset, mass, width, height, jointOffset, bodytoJoint, collide)
        self.setShape()
        # self.shape.filter = self.parent.armMask


class Leg(BodyPart_WithJoint):
    def __init__(self, parent, offset, mass, width, height, jointOffset, bodytoJoint, collide=True):
        super().__init__(parent, offset, mass, width, height, jointOffset, bodytoJoint, collide)

        self.joint_pos = (self.bodytoJoint.position[0] + self.joint_offset[0],
                          self.bodytoJoint.position[1] + self.joint_offset[1])
        self.joint = pymunk.RotaryLimitJoint(self.body, self.bodytoJoint, -0.3, 0.3)
        self.joint.collide_bodies = collide
        self.space.add(self.joint)
        self.setShape()
        self.shape.filter = self.parent.legMask
