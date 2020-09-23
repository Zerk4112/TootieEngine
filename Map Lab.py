import sys
import pygame.color
from pygame.locals import *
import pymunk.pygame_util
from data.ui.MapUIOverlay import *
from data.ui.Camera import *

# Game Settings

# Physics Constants
pymunk.pygame_util.positive_y_is_up = False
GRAVITY_VECTOR = (0.0, 900.0)
PLAYER_VELOCITY = 100. * 2.
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

# Pygame Constants
PYGAME_FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 900
SCREEN_CENTER = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
MAP_WIDTH, MAP_HEIGHT = 1200, 900
MAP_CENTER = MAP_WIDTH / 2, MAP_HEIGHT / 2
# Global Value Defaults


class Engine:
    def __init__(self):
        # Define Constants
        self.UIOffset = (0, 100)
        self._running = True
        self._run_physics = True

        # Define initial frame count
        self.frameCount = 0

        # Define screen to draw all surfaces on
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        ## Define surface to draw everything onto
        self.GameSurface = pygame.Surface([MAP_WIDTH, MAP_HEIGHT - self.UIOffset[1]])
        self.GameSurface_rect = self.GameSurface.get_rect()

        self.draw_options = pymunk.pygame_util.DrawOptions(self.GameSurface)
        pygame.display.set_caption("~~~ TootieEngine Map Laboratory ~~~")
        # Create space and init pygame
        self.guiOverlay = UISurface(SCREEN_WIDTH, self.UIOffset[1], self.screen)

        # Define camera object
        self.camera = CameraSurface(SCREEN_WIDTH, SCREEN_HEIGHT - self.UIOffset[1], self.GameSurface, (0, 0))
        pass
    def physicsTick(self):
        if self._run_physics:
            dt = PHYSICS_STEP / PHYSICS_FPS  # TODO: Enable the pausing of physics
            for x in range(1):
                self.space.step(dt)

    def on_init(self):
        self.space = pymunk.Space()
        self.space.gravity = GRAVITY_VECTOR
        pygame.init()
        self.clock = pygame.time.Clock()
        self._running = True

    def on_loop(self):
        self.physicsTick()
        self.camera.update_pos()
        pass

    def on_event(self, event):
        self.quit_check(event)
        self.camera.controller(event)

        pass

    def on_render(self):
        # Fill with white
        self.screen.fill((255, 255, 255))
        self.GameSurface.fill((120, 120, 120))
        self.guiOverlay.on_render()
        self.camera.update_render()
        self.camera.draw_render()
        self.screen.blit(self.GameSurface, self.UIOffset)
        pygame.display.flip()
        pygame.display.update()
        self.clock.tick(PYGAME_FPS)
        self.frameCount += 1

        pass

    def on_cleanup(self):
        pygame.quit()
        sys.exit()

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
        pass

    def quit_check(self, event):
        if event.type == QUIT:
            self._running = False

        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self._running = False
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    TootieEngine = Engine()
    TootieEngine.on_execute()