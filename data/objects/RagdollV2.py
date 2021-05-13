import pymunk


class RagdollV2:
    def __init__(self, space, pos):
        self.space = space
        self.limbMask = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b110, categories=0b110)
        self.torsoFilter = pymunk.ShapeFilter(categories=0b110)
        self.default_friction = 0.99
        self.default_moment_multiplier = 350
        self.origin_point = pos

        # Define body parts
        self.upperTorso = UpperTorso(self, (0, 0), 200, 40, 60, (0, 0))
        self.lowerTorso = LowerTorso(self, (0, 25), 100, 60, 25, (0, 16))
        self.leftArm = Arm(self, (-55, -20), 75, 65, 15, (-25, -20))
        self.rightArm = Arm(self, (55, -20), 75, 65, 15, (25, -20))
        self.leftLeg = Leg(self, (-12, 72), 75, 15, 65, (-11, 12))
        self.rightLeg = Leg(self, (12, 72), 75, 15, 65, (11, 12))
        self.head = Head(self, (0, -45), 200, 40, 60, (0, -30))

        pass

    def addToSpace(self):
        self.upperTorso.addToSpace()
        self.lowerTorso.addToSpace()
        self.leftArm.addToSpace()
        self.rightArm.addToSpace()
        self.leftLeg.addToSpace()
        self.rightLeg.addToSpace()
        self.head.addToSpace()


class BodyPart:
    def __init__(self, parent, offset, mass, width, height, jointOffset):
        self.offset = offset
        self.joint_offset = jointOffset
        self.parent = parent
        self.space = self.parent.space
        self.width, self.height = 40, 60
        self.vertices = [(-width / 2, -height / 2),
                         (width / 2, -height / 2),
                         (width / 2, height / 2),
                         (-width / 2, height / 2)]
        self.friction = self.parent.default_friction
        self.body = pymunk.Body(mass, mass * parent.default_moment_multiplier, body_type=pymunk.Body.DYNAMIC)
        self.body.position = (self.parent.origin_point[0] + offset[0], self.parent.origin_point[1] + offset[1])

    def addToSpace(self):
        self.space.add(self.body, self.shape)

    def setJointPos(self):
        self.joint_pos = (self.parent.Torso.body.position[0] + self.joint_offset[0],
                          self.parent.Torso.body.position[1] + self.joint_offset[1])

    def createJoint(self):
        self.joint = pymunk.PivotJoint(self.body, self.parent.Torso.body, self.joint_pos)
        self.space.add(self.joint)

    def setShape(self):
        self.shape = pymunk.Poly(self.body, self.vertices)
        self.shape.friction = self.parent.default_friction


class Head(BodyPart):
    def __init__(self, parent, offset, mass, width, height, jointOffset):
        super().__init__(parent, offset, mass, width, height, jointOffset)
        self.setShape()

        self.setJointPos()
        self.createJoint()

    def setShape(self):
        self.shape = pymunk.Circle(self.body, 15)
        self.shape.friction = self.parent.default_friction


class UpperTorso(BodyPart):
    def __init__(self, parent, offset, mass, width, height, jointOffset):
        super().__init__(parent, offset, mass, width, height, jointOffset)
        self.vertices = [(-width / 2, -height / 2), (width / 2, -height / 2),
                         (width / 3, height / 4), (-width / 3, height / 4)]
        self.setShape()
        self.shape.filter = self.parent.torsoFilter


class LowerTorso(BodyPart):
    def __init__(self, parent, offset, mass, width, height, jointOffset):
        super().__init__(parent, offset, mass, width, height, jointOffset)
        self.vertices = [(-width / 4, -height / 4),
                         (width / 4, -height / 4),
                         (width / 3, height / 2),
                         (-width / 3, height / 2)]
        self.setShape()
        self.shape.filter = self.parent.torsoFilter

        self.setJointPos()
        self.createJoint()


class Arm(BodyPart):
    def __init__(self, parent, offset, mass, width, height, jointOffset):
        super().__init__(parent, offset, mass, width, height, jointOffset)
        self.setShape()
        self.shape.filter = self.parent.limbMask

        self.setJointPos()
        self.createJoint()


class Leg(BodyPart):
    def __init__(self, parent, offset, mass, width, height, jointOffset):
        super().__init__(parent, offset, mass, width, height, jointOffset)
        self.setShape()
        self.shape.filter = self.parent.limbMask

        self.setJointPos()
        self.createJoint()

    def setJointPos(self):
        self.joint_pos = (self.parent.lowerTorso.body.position[0] + self.joint_offset[0],
                          self.parent.lowerTorso.body.position[1] + self.joint_offset[1])
