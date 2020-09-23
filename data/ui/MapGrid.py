import math
import pygame
from pygame.color import *

def simple_get_distance(point_1, point_2):
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)

class MapGrid:
    def __init__(self, mapSize, surface):
        self.surface = surface
        self.current_grid_spacing = 16
        self.minimum_grid_spacing = 16
        self.maximum_grid_spacing = 64
        self.spacing_muiltiplier = 2
        self.default_color = THECOLORS['white']
        self.center_color = THECOLORS['chocolate4']
        self.spacingVector = (
            (int(mapSize[0] / self.current_grid_spacing)), (int(mapSize[1] / self.current_grid_spacing)))
        self.selected_point = None
        self.drawToggle = True