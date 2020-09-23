import pygame

class UISurface:
    def __init__(self, width, height, surface):
        self.width = width
        self.height = height
        self.surface = surface
        self.UIDisplay = pygame.Surface([width, height])
        self.UIDisplay_rect = self.UIDisplay.get_rect()

    def on_render(self):
        # Fill UI Display with green
        self.UIDisplay.fill((0, 255, 0))
        # Draw Border
        pygame.draw.rect(self.UIDisplay, (0, 0, 0), self.UIDisplay_rect, 4)
        # Blit UIDisplay to surface
        self.surface.blit(self.UIDisplay, (0, 0))
