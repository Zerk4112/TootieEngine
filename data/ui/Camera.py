import pygame
from pygame.locals import *
import math

def simple_get_distance(point_1, point_2):
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)

class CameraSurface:
    def __init__(self, width, height, surface, screen_offset):
        self.offset = screen_offset
        self.width = width
        self.height = height
        self.center = screen_offset
        self.surface = surface
        self.cameraDisplay = pygame.Surface([width, height])
        self.cameraDisplay_rect = self.cameraDisplay.get_rect()
        self.x = screen_offset[0]
        self.y = screen_offset[1]
        self.angle = 0
        self.angleVel = 0
        self.xVel = 0
        self.yVel = 0
        self.following = True

    def update_render(self):
        # Fill UI Display with gray
        self.cameraDisplay.fill((120, 120, 120))
        # Draw Border
        pygame.draw.rect(self.cameraDisplay, (0, 0, 0), self.cameraDisplay_rect, 4)

    def draw_render(self):
        # Blit UIDisplay to surface
        self.surface.blit(self.cameraDisplay, (self.x, self.y))

    def update_pos(self):
        self.x += self.xVel
        self.y += self.yVel
        self.angle += self.angleVel

    def controller(self, event):

        if event.type == KEYDOWN and event.key == K_UP:
            self.yVel = 10
        if event.type == KEYUP and event.key == K_UP:
            self.yVel = 0

        if event.type == KEYDOWN and event.key == K_DOWN:
            self.yVel = -10
        if event.type == KEYUP and event.key == K_DOWN:
            self.yVel = 0

        if event.type == KEYDOWN and event.key == K_LEFT:
            self.xVel = 10
        if event.type == KEYUP and event.key == K_LEFT:
            self.xVel = 0

        if event.type == KEYDOWN and event.key == K_RIGHT:
            self.xVel = -10
        if event.type == KEYUP and event.key == K_RIGHT:
            self.xVel = 0

        if event.type == KEYDOWN and event.key == K_q:
            self.angleVel = -10
        if event.type == KEYUP and event.key == K_q:
            self.angleVel = 0

        if event.type == KEYDOWN and event.key == K_e:
            self.angleVel = 10
        if event.type == KEYUP and event.key == K_e:
            self.angleVel = 0

        if event.type == KEYDOWN and event.key == K_f:
            self.following = not self.following

    def follow(self, target):

        # offset calculation:
        # -target.body.position + self.center
        # speed = distance between camera and target / 2
        distance = simple_get_distance((self.x, self.y), (-target.body.position[0] + self.center[0], -target.body.position[1] + self.center[1]))
        self.camera_speed = distance / 32
        self.camera_safeZone = distance / 46
        if self.following:
            if self.x > -target.body.position[0] + self.center[0] - self.camera_safeZone:
                self.x -= self.camera_speed
            if self.x < -target.body.position[0] + self.center[0] - self.camera_safeZone:
                self.x += self.camera_speed

            if self.y > -target.body.position[1] + self.center[1] - self.camera_safeZone:
                self.y -= self.camera_speed
            if self.y < -target.body.position[1] + self.center[1] - self.camera_safeZone:
                self.y += self.camera_speed

            # self.x = -target.body.position[0] + (self.center[0])
            # self.y = -target.body.position[1] + (self.center[1])
            # print(f'Camera POS: {-target.body.position[0]}, {-target.body.position[1]}')
            # print(f'Target POS: {self.x}, {self.y}')
            # print(f'Set Offset: {self.center}')
