import sys
import pygame.color
from pygame.locals import *
import pymunk.pygame_util

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
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN_CENTER = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2

# Global Value Defaults


class Engine:
    def __init__(self):
        # Define Constants
        self._running = True
        self._run_physics = True

        self.frameCount = 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        pygame.display.set_caption("Object Oriented Template")
        # Create space and init pygame

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
        pass

    def on_event(self, event):
        self.quit_check(event)
        pass

    def on_render(self):
        # Fill with white
        self.screen.fill((255, 255, 255))


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