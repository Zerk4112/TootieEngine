import pygame
import pymunk

class DummyV1:
    def __init__(self, space, pos):
        self.default_friction = 0.99
        self.space = space
        self.moment_multiplier = 350
        # self.space.add_collosion_handler(1, 2).begin = self.collision_handler
        self.limbMask = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b1, categories=0b1)
        self.torsoFilter = pymunk.ShapeFilter(categories=0b1)
        self.head_radius = 15

        # Part offsets, relative to the center of the body (which is the upper torso)
        self.head_relOffset = (0, -self.head_radius * 3)
        self.upperTorso_relOffset = (0, 0)
        self.lowerTorso_relOffset = (0, 25)

        self.leftArm_relOffset = (-55, -20)
        self.rightArm_relOffset = (55, -20)

        self.leftLeg_relOffset = (-12, 72)
        self.rightLeg_relOffset = (12, 72)

        # Constraint Offsets
        # Neck
        self.head_neckOffset = (0, 10)
        self.upperTorso_neckOffset = (0, -30)

        # Shoulders
        self.leftArm_leftShoulderOffset = (30, 0)
        self.rightArm_rightShoulderOffset = (-30, 0)
        self.upperTorso_leftShoulderOffset = (-25, -20)
        self.upperTorso_rightShoulderOffset = (25, -20)

        # Hips
        self.upperTorso_leftLowerTorsoOffset = (0, 16)
        self.upperTorso_rightLowerTorsoOffset = (0, 16)

        # Legs
        self.lowerTorso_leftLegOffset = (-11, 12)
        self.lowerTorso_rightLegOffset = (11, 12)


        # Head - Physical Object Information
        self.head_mass = 65
        self.head_moment = self.head_mass * self.moment_multiplier
        self.head_body = pymunk.Body(self.head_mass, self.head_moment, body_type=pymunk.Body.DYNAMIC)
        self.head_body.position = (pos[0] + self.head_relOffset[0], pos[1] + self.head_relOffset[1])  # Set position to given position + box_offset
        self.head_shape = pymunk.Circle(self.head_body, self.head_radius)
        self.head_shape.friction = self.default_friction

        # Upper Torso - Physical Object Information
        self.upperTorso_mass = 200
        self.upperTorso_moment = self.upperTorso_mass * self.moment_multiplier
        self.upperTorsoWidth, self.upperTorsoHeight = 40, 60
        self.upperTorsoVertices = [(-self.upperTorsoWidth / 2, -self.upperTorsoHeight / 2), (self.upperTorsoWidth / 2, -self.upperTorsoHeight / 2),
                                   (self.upperTorsoWidth / 3, self.upperTorsoHeight / 4), (-self.upperTorsoWidth / 3, self.upperTorsoHeight / 4)]
        self.upperTorso_body = pymunk.Body(self.upperTorso_mass, self.upperTorso_moment, body_type=pymunk.Body.DYNAMIC)
        self.upperTorso_body.position = (pos[0] + self.upperTorso_relOffset[0], pos[1] + self.upperTorso_relOffset[1])
        self.upperTorso_shape = pymunk.Poly(self.upperTorso_body, self.upperTorsoVertices)
        self.upperTorso_shape.filter = self.torsoFilter
        self.upperTorso_shape.friction = self.default_friction

        # Lower Torso - Physical Object Information
        self.lowerTorso_mass = 100
        self.lowerTorso_moment = self.lowerTorso_mass * self.moment_multiplier
        self.lowerTorsoWidth, self.lowerTorsoHeight = 60, 25
        self.lowerTorsoVertices = [(-self.lowerTorsoWidth / 4, -self.lowerTorsoHeight / 4),
                                   (self.lowerTorsoWidth / 4, -self.lowerTorsoHeight / 4),
                                   (self.lowerTorsoWidth / 3, self.lowerTorsoHeight / 2),
                                   (-self.lowerTorsoWidth / 3, self.lowerTorsoHeight / 2)]
        self.lowerTorso_body = pymunk.Body(self.lowerTorso_mass, self.lowerTorso_moment, body_type=pymunk.Body.DYNAMIC)
        self.lowerTorso_body.position = (pos[0] + self.lowerTorso_relOffset[0], pos[1] + self.lowerTorso_relOffset[1])
        self.lowerTorso_shape = pymunk.Poly(self.lowerTorso_body, self.lowerTorsoVertices)
        self.lowerTorso_shape.filter = self.torsoFilter
        self.lowerTorso_shape.friction = self.default_friction

        # Left Arm - Physical Object Information
        self.leftArm_mass = 75
        self.leftArm_moment = self.leftArm_mass * self.moment_multiplier
        self.leftArmWidth, self.leftArmHeight = 65, 15
        self.leftArmVertices = [(-self.leftArmWidth / 2, -self.leftArmHeight / 2),
                                   (self.leftArmWidth / 2, -self.leftArmHeight / 2),
                                   (self.leftArmWidth / 2, self.leftArmHeight / 2),
                                   (-self.leftArmWidth / 2, self.leftArmHeight / 2)]
        self.leftArm_body = pymunk.Body(self.leftArm_mass, self.leftArm_moment, body_type=pymunk.Body.DYNAMIC)
        self.leftArm_body.position = (pos[0] + self.leftArm_relOffset[0], pos[1] + self.leftArm_relOffset[1])
        self.leftArm_shape = pymunk.Poly(self.leftArm_body, self.leftArmVertices)
        self.leftArm_shape.filter = self.limbMask
        self.leftArm_shape.friction = self.default_friction

        # Right Arm - Physical Object Information
        self.rightArm_mass = 75
        self.rightArm_moment = self.rightArm_mass * self.moment_multiplier
        self.rightArmWidth, self.rightArmHeight = 65, 15
        self.rightArmVertices = [(-self.rightArmWidth / 2, -self.rightArmHeight / 2),
                                (self.rightArmWidth / 2, -self.rightArmHeight / 2),
                                (self.rightArmWidth / 2, self.rightArmHeight / 2),
                                (-self.rightArmWidth / 2, self.rightArmHeight / 2)]
        self.rightArm_body = pymunk.Body(self.rightArm_mass, self.rightArm_moment, body_type=pymunk.Body.DYNAMIC)
        self.rightArm_body.position = (pos[0] + self.rightArm_relOffset[0], pos[1] + self.rightArm_relOffset[1])
        self.rightArm_shape = pymunk.Poly(self.rightArm_body, self.rightArmVertices)
        self.rightArm_shape.filter = self.limbMask
        self.rightArm_shape.friction = self.default_friction

        # Left Leg - Physical Object Information
        self.leftLeg_mass = 80
        self.leftLeg_moment = self.leftLeg_mass * self.moment_multiplier
        self.leftLegWidth, self.leftLegHeight = 15, 65
        self.leftLegVertices = [(-self.leftLegWidth / 2, -self.leftLegHeight / 2),
                                 (self.leftLegWidth / 2, -self.leftLegHeight / 2),
                                 (self.leftLegWidth / 2, self.leftLegHeight / 2),
                                 (-self.leftLegWidth / 2, self.leftLegHeight / 2)]
        self.leftLeg_body = pymunk.Body(self.leftLeg_mass, self.leftLeg_moment, body_type=pymunk.Body.DYNAMIC)
        self.leftLeg_body.position = (pos[0] + self.leftLeg_relOffset[0], pos[1] + self.leftLeg_relOffset[1])
        self.leftLeg_shape = pymunk.Poly(self.leftLeg_body, self.leftLegVertices)
        self.leftLeg_shape.filter = self.limbMask
        self.leftLeg_shape.friction = self.default_friction

        # Right Leg - Physical Object Information
        self.rightLeg_mass = 80
        self.rightLeg_moment = self.rightLeg_mass * self.moment_multiplier
        self.rightLegWidth, self.rightLegHeight = 15, 65
        self.rightLegVertices = [(-self.rightLegWidth / 2, -self.rightLegHeight / 2),
                                (self.rightLegWidth / 2, -self.rightLegHeight / 2),
                                (self.rightLegWidth / 2, self.rightLegHeight / 2),
                                (-self.rightLegWidth / 2, self.rightLegHeight / 2)]
        self.rightLeg_body = pymunk.Body(self.rightLeg_mass, self.rightLeg_moment, body_type=pymunk.Body.DYNAMIC)
        self.rightLeg_body.position = (pos[0] + self.rightLeg_relOffset[0], pos[1] + self.rightLeg_relOffset[1])
        self.rightLeg_shape = pymunk.Poly(self.rightLeg_body, self.rightLegVertices)
        self.rightLeg_shape.filter = self.limbMask
        self.rightLeg_shape.friction = self.default_friction

    def addToSpace(self):
        # Add Head
        self.space.add(self.head_body, self.head_shape)

        # Torso
        self.space.add(self.upperTorso_body, self.upperTorso_shape)
        self.space.add(self.lowerTorso_body, self.lowerTorso_shape)

        # Arms
        self.space.add(self.leftArm_body, self.leftArm_shape)
        self.space.add(self.rightArm_body, self.rightArm_shape)

        # Legs
        self.space.add(self.leftLeg_body, self.leftLeg_shape)
        self.space.add(self.rightLeg_body, self.rightLeg_shape)

        # Joints
        # Neck
        self.neckConstraint = pymunk.PivotJoint(self.head_body, self.upperTorso_body, (
        (self.upperTorso_body.position.x + self.upperTorso_neckOffset[0]),
        (self.upperTorso_body.position[1] + self.upperTorso_neckOffset[1])))
        self.space.add(self.neckConstraint)

        # Arms
        self.leftArmConstraint = pymunk.PivotJoint(self.leftArm_body, self.upperTorso_body, (
        (self.upperTorso_body.position.x + self.upperTorso_leftShoulderOffset[0]),
        (self.upperTorso_body.position[1] + self.upperTorso_leftShoulderOffset[1])))
        self.rightArmConstraint = pymunk.PivotJoint(self.rightArm_body, self.upperTorso_body, (
        (self.upperTorso_body.position.x + self.upperTorso_rightShoulderOffset[0]),
        (self.upperTorso_body.position[1] + self.upperTorso_rightShoulderOffset[1])))
        # self.leftArmConstraint.max_force = 50000 ** 50
        # self.leftArmConstraint.max_bias = 20 ** 60
        # self.leftArmConstraint.error_bias = 0
        self.space.add(self.leftArmConstraint, self.rightArmConstraint)

        # Hips
        self.leftHipConstraint = pymunk.PivotJoint(self.lowerTorso_body, self.upperTorso_body, (
        (self.upperTorso_body.position.x + self.upperTorso_leftLowerTorsoOffset[0]),
        (self.upperTorso_body.position[1] + self.upperTorso_leftLowerTorsoOffset[1])))
        self.RightHipConstraint = pymunk.PivotJoint(self.lowerTorso_body, self.upperTorso_body, (
        (self.upperTorso_body.position.x + self.upperTorso_rightLowerTorsoOffset[0]),
        (self.upperTorso_body.position[1] + self.upperTorso_rightLowerTorsoOffset[1])))
        self.space.add(self.leftHipConstraint, self.RightHipConstraint)

        # Legs
        self.leftLegConstraint = pymunk.PivotJoint(self.leftLeg_body, self.lowerTorso_body, (
        (self.lowerTorso_body.position.x + self.lowerTorso_leftLegOffset[0]),
        (self.lowerTorso_body.position[1] + self.lowerTorso_leftLegOffset[1])))
        self.rightLegConstraint = pymunk.PivotJoint(self.rightLeg_body, self.lowerTorso_body, (
        (self.lowerTorso_body.position.x + self.lowerTorso_rightLegOffset[0]),
        (self.lowerTorso_body.position[1] + self.lowerTorso_rightLegOffset[1])))
        self.space.add(self.leftLegConstraint, self.rightLegConstraint)

