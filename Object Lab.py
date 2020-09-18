import sys
import pygame
from pygame.locals import *
import pygame.color
import pymunk.pygame_util
from data.objects.Geometry import *
from data.ToolBox import *
from data.ToolBoxOverlay import *
from data.objects.RagdollV2 import *
from data.objects.RagdollV5 import *

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
        self.UIOffset = (0, 50)

        self.space = pymunk.Space()
        self.space.gravity = GRAVITY_VECTOR
        self.mouseTools = ToolBox(self.space, self.UIOffset)
        self.toolsOverlay = ToolsOverlay(SCREEN_WIDTH, self.UIOffset[1], self.mouseTools)
        self._running = True
        self._run_physics = False
        self.frameCount = 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # self.UISurface = pygame.Surface([SCREEN_WIDTH, self.UIOffset[1]])
        self.GameSurface = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT - self.UIOffset[1]])
        self.GameSurface_rect = self.GameSurface.get_rect()


        self.draw_options = pymunk.pygame_util.DrawOptions(self.GameSurface)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("~~~ TootieEngine Laboratory ~~~")
        # Create space and init pygame

    def physicsTick(self):
        if self._run_physics:
            dt = PHYSICS_STEP / PHYSICS_FPS  # TODO: Enable the pausing of physics
            for x in range(1):
                self.space.step(dt)

    def on_init(self):
        pygame.init()
        self._running = True

        # Define Room walls
        self.ceiling = KinematicBoundary((0, 0), (SCREEN_WIDTH, 0), 20, (0, 0, 0))
        self.floor = KinematicBoundary((0, SCREEN_CENTER[1] + 250), (SCREEN_WIDTH, SCREEN_CENTER[1] + 250), 20, (0, 0, 0))
        self.leftWall = KinematicBoundary((0, 0), (0, SCREEN_HEIGHT), 20, (0, 0, 0))
        self.rightWall = KinematicBoundary((SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), 20, (0, 0, 0))

        self.ceiling.addToSpace(self.space)
        self.floor.addToSpace(self.space)
        self.leftWall.addToSpace(self.space)
        self.rightWall.addToSpace(self.space)

        # self.ragdoll1 = RagdollV2(self.space, (self.GameSurface_rect.center[0] - 250, self.GameSurface_rect.center[1]))
        # self.ragdoll1.addToSpace()

        self.ragdoll2 = RagdollV4(self.space, (self.GameSurface_rect.center[0] + 250, self.GameSurface_rect.center[1]))
        self.ragdoll2.addToSpace()

    def on_loop(self):
        self.mouseTools.update_pos()
        self.ragdoll2.upperTorso.standup()
        self.ragdoll2.on_loop()
        # print(self.ragdoll2.head.body.velocity)
        pass

    def on_event(self, event):
        self.quit_check(event)
        self.mouseTools.on_event(event)
        self.physicsToggle(event)
        self.ragdoll2.on_event(event)
        pass

    def on_render(self):
        # Fill screen with white color
        self.screen.fill((255, 255, 255))
        self.toolsOverlay.on_render(self.screen)
        self.GameSurface.fill((120, 120, 120))
        # Draw the mouse tool
        self.space.debug_draw(self.draw_options)
        self.mouseTools.draw(self.GameSurface)



        self.screen.blit(self.GameSurface, self.UIOffset)
        # self.platform.draw(self.screen)

        pygame.display.flip()
        if self._run_physics:
            self.physicsTick()
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
    def physicsToggle(self, event):
        if event.type == KEYDOWN and event.key == K_p:
            self._run_physics = not self._run_physics


if __name__ == "__main__":
    TootieEngine = Engine()
    TootieEngine.on_execute()
