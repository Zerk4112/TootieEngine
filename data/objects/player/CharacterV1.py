import pygame
from pygame.locals import *
import pymunk
import math
from pymunk import Vec2d
from data.objects.player.BodyParts import *
import pymunk.pygame_util
PLAYER_VELOCITY = 100. * 1.5
PLAYER_GROUND_ACCEL_TIME = 0.05
PLAYER_GROUND_ACCEL = (PLAYER_VELOCITY / PLAYER_GROUND_ACCEL_TIME)
PLAYER_AIR_ACCEL_TIME = 0.25
PLAYER_AIR_ACCEL = (PLAYER_VELOCITY / PLAYER_AIR_ACCEL_TIME)
JUMP_HEIGHT = 16. * 3
JUMP_BOOST_HEIGHT = 24.
JUMP_CUTOFF_VELOCITY = 100
FALL_VELOCITY = 250.
JUMP_LENIENCY = 0.05
HEAD_FRICTION = 0.7
PLATFORM_SPEED = 1
PHYSICS_STEP = 1.0
PHYSICS_FPS = 60.0
dt = PHYSICS_STEP / PHYSICS_FPS

def cpfclamp(f, min_, max_):
    """Clamp f between min and max"""
    return min(max(f, min_), max_)


# Other kinds of math
def cpflerpconst(f1, f2, d):
    """Linearly interpolate from f1 to f2 by no more than d."""
    return f1 + cpfclamp(f2 - f1, -d, d)

class PlayerV1:
    def __init__(self, space, pos, surface):
        self.surface = surface
        self.armMask = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b1, categories=0b1)
        self.legMask = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b1, categories=0b1)
        self.torsoFilter = pymunk.ShapeFilter(categories=0b1)
        self.space = space
        self.body = pymunk.Body(250, pymunk.inf)
        self.body.position = pos
        self.spawn_position = pos
        self.xVel = 0
        self.yVel = 0
        self.body.friction = 5

        self.direction = 1
        self.remaining_jumps = 2
        self.landing = {'p': Vec2d.zero(), 'n': 0}
        self.landed_previous = False
        self.grounding = {
            'normal': Vec2d.zero(),
            'penetration': Vec2d.zero(),
            'impulse': Vec2d.zero(),
            'position': Vec2d.zero(),
            'body': None
        }
        self.K_wPressed = False
        self.K_aPressed = False
        self.K_sPressed = False
        self.K_dPressed = False
        self.target_vx = 0
        self.head = CharacterPartCircle(self, (0, 0, 255), (0, -40), 20, 1)
        self.Torso = CharacterPartSquare(self, (0, 255, 0), (0, -200), 8, 25, 1, [(-16 / 2, -35), (16 / 2, -35), (16, 35), (-16, 35)])
        # self.leftArm = Arms()
        # self.Legs = CharacterPartSegment(self, (0, 255, 0), (0, 60), 6, 35, 0)
        # self.upperArm = Arms(self, (0, 0, 0), (20, -20), (0, -20), self.body, 1, 20, 6, False)
        # self.lowerArm = Arms(self, (0, 0, 0), (55, -20), (20, 0), self.upperArm.body, 1, 20, 6, False)
        self.leftUpperLeg = Legs(self, (0, 0, 0), (0, 55), (0, 40), self.body, 1, 6, 20, 50, False)
        self.leftUpperLegLimiter = RotationLimiter(self.space, self.leftUpperLeg.body, self.body, (0, 0), -1, 1, False)

        self.leftLowerLeg = Legs(self, (0, 0, 0), (0, 95), (0, 20), self.leftUpperLeg.body, 1, 6, 20, 100, False)
        self.leftLowerLegLimiter = RotationLimiter(self.space, self.leftUpperLeg.body, self.leftLowerLeg.body, (0, 0), -0.5, 0.5, False)

        self.rightUpperLeg = Legs(self, (0, 0, 0), (0, 55), (0, 40), self.body, 1, 6, 20, 50,False)
        self.rightUpperLegLimiter = RotationLimiter(self.space, self.rightUpperLeg.body, self.body, (0, 0), -1, 1, False)


        self.rightLowerLeg = Legs(self, (0, 0, 0), (0, 95), (0, 20), self.rightUpperLeg.body, 1, 6, 20, 100,False)
        self.rightLowerLegLimiter = RotationLimiter(self.space, self.rightLowerLeg.body, self.rightUpperLeg.body, (0, 0), -0.5, 0.5, False)
        self.standing_joint = SpaceJoint(self.space, self, self.body)
        self.current_leg_cycle = self.rightLowerLeg
        # self.leftLowerLeg = Legs(self, (0, 0, 0), (0, -0), (0, 40), self.leftUpperLeg.body, 1, 6, 20, False)

        self.walk_right = False
        self.walk_left = False
        self.lastStep = None
        self.lastLeg = 'right'


    def on_loop(self):
        # self.leftUpperLeg.body.angle = -0.5
        # self.rightUpperLeg.body.angle = 0.5
        self.update_direction()
        self.standing_joint.update_pos()
        self.clear_arbiter_dictionary()
        self.leftLowerLeg.body.each_arbiter(self.refresh_arbiter_dictionary)
        self.rightLowerLeg.body.each_arbiter(self.refresh_arbiter_dictionary)

        self.walk_cycle()

        self.check_grounding()
        self.landing_check(self.surface)
        self.leftLowerLeg.shape.friction = 1
        self.rightLowerLeg.shape.friction = 1
        print(self.leftLowerLeg.shape.friction)

    def walk_cycle(self):
        if self.lastStep is not None:
            currentTick = pygame.time.get_ticks()
            time_since_walkStart = currentTick - self.lastStep
            # print(time_since_jointStart)
            if time_since_walkStart > 120:
                if self.lastLeg == 'right':
                    # self.leftUpperLeg.body.apply_impulse_at_local_point((self.xVel * 10, 0), (0, 50))
                    self.leftLowerLeg.body.apply_impulse_at_local_point((self.xVel * 5, 0), (0, 0))
                    self.lastLeg = 'left'
                    self.lastStep = currentTick
                elif self.lastLeg == 'left':
                    # self.rightUpperLeg.body.apply_impulse_at_local_point((self.xVel * 10, 0), (0, 100))
                    self.rightLowerLeg.body.apply_impulse_at_local_point((self.xVel * 5, 0), (0, 0))
                    self.lastStep = currentTick
                    self.lastLeg = 'right'

    def controller(self, event):
        current_tick = pygame.time.get_ticks()
        self.jump_handler(event)
        angleVel = 0.5
        impule_vel = 100 * 25
        if event.type == KEYDOWN and event.key == K_w:
            pass
            # self.yVel -= 100 * 50
            # self.leftLowerLeg.body.apply_impulse_at_local_point((0, 0), (0, 0))
        if event.type == KEYUP and event.key == K_w:
            pass
            # self.yVel -= 0

        # if event.type == KEYDOWN and event.key == K_s:
        #     # self.leftLowerLeg.body.apply_impulse_at_local_point((100 * 99, 0), (0, 0))
        #
        # if event.type == KEYUP and event.key == K_s:
        #     self.leftUpperLeg.body.angle += 0

        if event.type == KEYDOWN and event.key == K_a:
            self.lastStep = current_tick
            self.xVel = -impule_vel
            self.walk_left = True
            # self.leftLowerLeg.body.apply_impulse_at_local_point((100 * 99, 0), (0, 0))
        if event.type == KEYUP and event.key == K_a:
            self.lastStep = None
            self.xVel = 0
            self.walk_left = False

        if event.type == KEYDOWN and event.key == K_d:
            self.lastStep = current_tick
            self.xVel = impule_vel
            self.walk_right = True

            # self.leftLowerLeg.body.apply_impulse_at_local_point((100 * 99, 0), (0, 0))
        if event.type == KEYUP and event.key == K_d:
            self.lastStep = None
            self.xVel = 0
            self.walk_right = False



    def addToSpace(self):
        self.space.add(self.body, self.head.shape, self.Torso.shape)
        # self.space.add(self.upperArm.body, self.upperArm.shape, self.upperArm.joint)
        # self.space.add(self.lowerArm.body, self.lowerArm.shape, self.lowerArm.joint)
        self.space.add(self.leftUpperLeg.body, self.leftUpperLeg.shape, self.leftUpperLeg.joint)
        self.space.add(self.leftLowerLeg.body, self.leftLowerLeg.shape, self.leftLowerLeg.joint)

        self.space.add(self.rightUpperLeg.body, self.rightUpperLeg.shape, self.rightUpperLeg.joint)
        self.space.add(self.rightLowerLeg.body, self.rightLowerLeg.shape, self.rightLowerLeg.joint)

    def clear_arbiter_dictionary(self):
        self.grounding = {
            'normal': Vec2d.zero(),
            'penetration': Vec2d.zero(),
            'impulse': Vec2d.zero(),
            'position': Vec2d.zero(),
            'body': None
        }

    def refresh_arbiter_dictionary(self, arbiter):
        n = arbiter.contact_point_set.normal
        if n.y > self.grounding['normal'].y:
            self.grounding['normal'] = n
            self.grounding['penetration'] = -arbiter.contact_point_set.points[0].distance
            self.grounding['body'] = arbiter.shapes[1].body
            self.grounding['impulse'] = arbiter.total_impulse
            self.grounding['position'] = arbiter.contact_point_set.points[0].point_b

    def check_grounding(self):
        self.well_grounded = False
        if self.grounding['body'] != None:
            self.grounding_check = abs(self.grounding['normal'].x / self.grounding['normal'].y)
            if self.grounding_check < self.leftLowerLeg.shape.friction or self.grounding_check < self.rightLowerLeg.shape.friction:

                self.well_grounded = True
                self.remaining_jumps = 2
        self.ground_velocity = Vec2d.zero()
        if self.well_grounded:
            self.ground_velocity = self.grounding['body'].velocity

        # Walk cycle
        # if self.current_leg_cycle.body.angle > 1 or self.current_leg_cycle.body.angle < -1:
        #     self.swap_legs()
        # self.current_leg_cycle.shape.surface_velocity = -self.target_vx, 0


        if self.grounding['body'] != None:
            self.leftLowerLeg.shape.friction = PLAYER_GROUND_ACCEL / self.space.gravity.y
            self.rightLowerLeg.shape.friction = PLAYER_GROUND_ACCEL / self.space.gravity.y

            self.head.friction = HEAD_FRICTION
        else:
            self.leftUpperLeg.shape.friction, self.head.friction = 0, 0
            self.rightUpperLeg.shape.friction, self.head.friction = 0, 0

        if self.well_grounded:
            self.standing_joint.add_joint()
        else:
            self.standing_joint.remove_joint()


        # # Air control
        # if self.grounding['body'] is None:
        #
        #     if self.K_aPressed is True or self.K_dPressed is True or self.K_sPressed is True or self.K_wPressed is True:
        #         self.body.velocity = Vec2d(
        #             cpflerpconst(self.body.velocity.x, self.target_vx + self.ground_velocity.x, PLAYER_AIR_ACCEL * dt),
        #             self.body.velocity.y)
        #
        #     self.body.velocity.y = max(self.body.velocity.y, -FALL_VELOCITY)  # clamp upwards as well?

    def update_direction(self):
        self.K_aPressed = False
        self.K_sPressed = False
        self.K_dPressed = False

        self.target_vx = 0
        if self.body.velocity.x > .01:
            self.direction = 1
        elif self.body.velocity.x < -.01:
            self.direction = -1
        self.keys = pygame.key.get_pressed()
        if self.keys[K_a]:
            self.K_aPressed = True

            self.direction = -1
            self.target_vx -= PLAYER_VELOCITY
        if self.keys[K_d]:
            self.K_dPressed = True

            self.direction = 1
            self.target_vx += PLAYER_VELOCITY
        if self.keys[K_s]:
            self.K_sPressed = True
            self.direction = -3
        # self.rightLowerLeg.shape.surface_velocity = -self.target_vx, 0
        # print(self.target_vx)


    def landing_check(self, screen):
        # Did we land?
        landing_mass = abs(self.grounding['impulse'].y) / self.body.mass
        # print(self.landing_mass)  # DEBUG
        if landing_mass > 200 and self.landed_previous is False:
            landing = {'p': self.grounding['position'], 'n': 5}
            self.landed_previous = True
        else:
            self.landed_previous = False
        if self.landing['n'] > 0:
            p = pymunk.pygame_util.to_pygame(self.landing['p'], screen)
            pygame.draw.circle(screen, pygame.color.THECOLORS['yellow'], p, 5)
            self.landing['n'] -= 1

    def jump_handler(self, event):
        if event.type == KEYDOWN and event.key == K_w:
            self.K_wPressed = True
            if self.well_grounded or self.remaining_jumps > 0:
                self.jump_v = math.sqrt(2.0 * JUMP_HEIGHT * abs(self.space.gravity.y))
                self.impulse = (0, self.body.mass * -(self.ground_velocity.y + self.jump_v))
                self.body.apply_impulse_at_local_point(self.impulse)
                if self.remaining_jumps == 2:
                    pass
                elif self.remaining_jumps == 1:
                    pass
                self.remaining_jumps -= 1


        elif event.type == KEYUP and event.key == K_w:
            self.K_wPressed = False
            self.body.velocity.y = min(self.body.velocity.y, JUMP_CUTOFF_VELOCITY)