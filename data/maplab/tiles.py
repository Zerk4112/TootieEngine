import pymunk


class AirTile:
    def __init__(self, rect, origin_point):
        self.width, self.height = rect[0], rect[1]
        self.x, self.y = origin_point[0], origin_point[1]
        self.center_point = (self.x - (self.width / 2), self.y - (self.height / 2))
        self.collision_type = 0

    def debugDraw(self):
