import pygame
from pygame.locals import *
import pymunk



class ToolsOverlay:

    def __init__(self, width, height, toolset):
        self.width = width
        self.height = height
        self.font_name = 'data/font.ttf'
        self.display_surface = pygame.Surface([width, height])
        self.display_rect = self.display_surface.get_rect()

        self.toolset = toolset

        self.toolset_surface = pygame.Surface([width / 3, height])
        self.toolset_rect = self.toolset_surface.get_rect()

        self.description_surface = pygame.Surface([width - (width / 3), height])
        self.description_rect = self.description_surface.get_rect()

    def renderText(self):
        yOffset = 15
        font = pygame.font.Font(self.font_name, 12)
        smallfont = pygame.font.Font(self.font_name, 10)
        if self.toolset.current_toolset is None:
            selected_toolset_text = f"Toolset: None"
        else:
            selected_toolset_text = f"Toolset: {self.toolset.current_toolset['name']}"
        if self.toolset.current_tool is not None:
            selected_tool_text = f"Tool: {self.toolset.current_tool['name']}"
            selected_description_text = f"{self.toolset.current_tool['description']}"
        else:
            selected_tool_text = f"Tool: None"
            if self.toolset.current_toolset is not None:
                selected_description_text = f"{self.toolset.current_toolset['description']}"
            else:
                selected_description_text = f"No Tool Selected."

        selected_toolset_text_surface = font.render(selected_toolset_text, True, (0, 0, 0))
        selected_toolset_text_rect = selected_toolset_text_surface.get_rect()
        selected_toolset_text_rect.center = (self.toolset_rect.center[0], yOffset)

        selected_tool_text_surface = font.render(selected_tool_text, True, (0, 0, 0))
        selected_tool_text_rect = selected_tool_text_surface.get_rect()
        selected_tool_text_rect.center = (self.toolset_rect.center[0], yOffset * 2)

        selected_description_text_surface = smallfont.render(selected_description_text, True, (0, 0, 0))
        selected_description_text_rect = selected_description_text_surface.get_rect()
        selected_description_text_rect.center= (self.description_rect.midtop[0], yOffset)

        self.toolset_surface.blit(selected_toolset_text_surface, selected_toolset_text_rect)
        self.toolset_surface.blit(selected_tool_text_surface, selected_tool_text_rect)
        self.description_surface.blit(selected_description_text_surface, selected_description_text_rect)

        pass


    def on_render(self, screen):
        # Fill surfaces with background colors
        self.display_surface.fill((0, 150, 150))
        self.toolset_surface.fill((44, 220, 197))
        self.description_surface.fill((100,100,50))

        # Draw Borders for windows
        pygame.draw.rect(self.display_surface, (0, 0, 0), self.display_rect, 4)
        pygame.draw.rect(self.toolset_surface, (0, 0, 0), self.toolset_rect, 4)
        pygame.draw.rect(self.description_surface, (0, 0, 0), self.description_rect, 4)

        # Blit to surfaces
        self.renderText()
        self.display_surface.blit(self.toolset_surface, (0,0))
        self.display_surface.blit(self.description_surface, (0 + self.width / 3,0))


        # Blit to main screen display
        screen.blit(self.display_surface, (0, 0))