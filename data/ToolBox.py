from pygame.locals import *
from data.objects.Basic_Shapes import *
from data.objects.RagdollV1 import *
from data.objects.RagdollV2 import *
from data.objects.RagdollV3 import *
from data.objects.RagdollV4 import *

class ToolBox:

    def __init__(self, space, offset):
        self.toolset_dict = {
            0: {
                "name": "Move",
                "description": "Toolset for moving objects",
                "tools": {
                    0: {
                        "name": "Grabber",
                        "description": "Grabs Objects using Pymunk PivotJoint.",
                        "tool": grabTool(self),
                        "params": None
                    }
                }
            },
            1: {
                "name": "Select",
                "description": "Toolset for selection objects.",
                "tools": {
                    0: {
                        "name": "Area Select",
                        "description": "Use a Rectangle to select multiple objects.",
                        "tool": None,
                        "params": None
                    },
                    1: {
                        "name": "Simple Select",
                        "description": "Use the cursor to select an object",
                        "tool": None,
                        "params": None
                    },
                }
            },
            2: {
                "name": "Create",
                "description": "Toolset for creating objects.",
                "tools": {
                    0: {
                        "name": "Ball",
                        "description": "Creates a ball",
                        "tool": createTool(self),
                        "params": "ball"
                    },
                    1: {
                        "name": "Square",
                        "description": "Creates a square",
                        "tool": createTool(self),
                        "params": "square"
                    },
                    2: {
                        "name": "RagdollV1",
                        "description": "Creates a basic Ragdoll(V1)",
                        "tool": createTool(self),
                        "params": "ragdollv1"
                    },
                    3: {
                        "name": "RagdollV2",
                        "description": "Creates a basic Ragdoll(V2)",
                        "tool": createTool(self),
                        "params": "ragdollv2"
                    },
                    4: {
                        "name": "RagdollV3",
                        "description": "Creates a basic Ragdoll(V3)",
                        "tool": createTool(self),
                        "params": "ragdollv3"
                    },
                    5: {
                        "name": "RagdollV4",
                        "description": "Creates a basic Ragdoll(V4)",
                        "tool": createTool(self),
                        "params": "ragdollv4"
                    },
                }
            },
        }
        self.space = space
        self.pos = (0, 0)

        self.radius = 8
        self.vertices = [(-self.radius / 2, -self.radius / 2), (self.radius / 2, -self.radius / 2),
                         (self.radius / 2, self.radius / 2), (-self.radius / 2, self.radius / 2), (-self.radius / 2, self.radius / 4)]
        self.radius_multiplier = 2
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.shape = pymunk.Circle(self.body, self.radius, (0, 0))
        # self.shape.collision_type = 1
        self.body.position = (0, 0)
        self.current_toolset = self.toolset_dict[0]
        self.current_tool = self.toolset_dict[0]["tools"][0]
        self.toolset_cycle = 0
        self.tool_cycle = 0
        self.offset_vector = offset
        self.isCircle = True
        # self.space.add(self.shape)
        self.camera_offset = (0, 0)

    def update_pos(self, camera_offset):
        mousePOS = pygame.mouse.get_pos()
        self.camera_offset = camera_offset
        self.pos = (mousePOS[0] - self.offset_vector[0] - self.camera_offset[0], mousePOS[1] - self.offset_vector[1] - self.camera_offset[1])
        self.body.position = self.pos

    def switch_cursor_shape(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 2:
            if self.isCircle:
                self.shape = pymunk.Poly(self.body, self.vertices)
                self.isCircle = False
            else:
                self.shape = pymunk.Circle(self.body, self.radius, (0, 0))
                self.isCircle = True


    def update_radius(self, event):

        if event.type == MOUSEBUTTONDOWN and event.button == 4:
            self.radius += 1
            self.vertices = [(-self.radius / 2, -self.radius / 2), (self.radius / 2, -self.radius / 2),
                             (self.radius / 2, self.radius / 2), (-self.radius / 2, self.radius / 2)]

            if self.isCircle:
                # self.space.remove(self.shape)
                self.shape = pymunk.Circle(self.body, self.radius, (0, 0))
                # self.space.add(self.shape)
            else:
                # self.space.remove(self.shape)
                self.shape = pymunk.Poly(self.body, self.vertices)
                # self.space.add(self.shape)
        if event.type == MOUSEBUTTONDOWN and event.button == 5:
            if self.radius > 1:
                self.radius -= 1
                self.vertices = [(-self.radius / 2, -self.radius / 2), (self.radius / 2, -self.radius / 2),
                                 (self.radius / 2, self.radius / 2), (-self.radius / 2, self.radius / 2)]

            if self.isCircle:
                # self.space.remove(self.shape)
                self.shape = pymunk.Circle(self.body, self.radius, (0, 0))
                # self.space.add(self.shape)
            else:
                # self.space.remove(self.shape)
                self.shape = pymunk.Poly(self.body, self.vertices)
                # self.space.add(self.shape)

        pass

    def switch_toolset(self, event):
        if event.type == KEYDOWN and event.key == K_KP_PLUS:
            self.toolset_cycle += 1
            if self.toolset_cycle > len(self.toolset_dict) - 1:
                self.toolset_cycle = 0
            self.current_toolset = self.toolset_dict[self.toolset_cycle]
            self.current_tool = None
        pass

    def switch_tool(self, event):
        if event.type == KEYDOWN and event.key == K_KP_MINUS:
            self.tool_cycle += 1
            if self.tool_cycle > len(self.toolset_dict[self.toolset_cycle]["tools"]) - 1:
                self.tool_cycle = 0
            self.current_tool = self.toolset_dict[self.toolset_cycle]["tools"][self.tool_cycle]
        pass

    def on_event(self, event):
        self.switch_toolset(event)
        self.switch_tool(event)
        # self.update_radius(event)
        self.switch_cursor_shape(event)
        if self.current_tool is not None:
            if self.current_tool["tool"] is not None:
                self.current_tool["tool"].event_handler(event)
        pass

    def draw(self, surface, offset):
        if self.isCircle:
            pygame.draw.circle(surface, (0, 0, 0), (int(self.body.position.x + offset[0]), int(self.body.position.y + offset[1])),self.radius)
        else:
            pygame.draw.rect(surface, (0, 0, 0), (int(self.body.position.x - (self.radius / 2)), int(self.body.position.y - (self.radius / 2)), self.radius, self.radius))
        pass


class selectTool:
    def __init__(self, parent):
        self.parent = parent

        pass

class createTool:
    def __init__(self, parent):
        self.parent = parent
        self.squarePoint1 = None
        self.squarePoint2 = None
        pass

    def event_handler(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.parent.current_tool["params"] == "ball":
                self.createBall()
            if self.parent.current_tool["params"] == "square":
                self.createSquare()
            if self.parent.current_tool["params"] == "ragdollv1":
                self.createRagdollV1()
            if self.parent.current_tool["params"] == "ragdollv2":
                self.createRagdollV2()
            if self.parent.current_tool["params"] == "ragdollv3":
                self.createRagdollV3()
            if self.parent.current_tool["params"] == "ragdollv4":
                self.createRagdollV4()

            print("did a thing")

    def createBall(self):
        mass = self.parent.radius * 1.2
        moment = mass ** 2.5
        ball = Ball(self.parent.body.position, self.parent.space, mass,  0.99, moment, (0, 0, 0), self.parent.radius)
        ball.addToSpace()

    def createSquare(self):
        mass = self.parent.radius * 1.2
        moment = mass ** 2.5
        square = Square(self.parent.body.position, self.parent.space, self.parent.radius,  0.99, moment, (0, 0, 0), self.parent.vertices)
        print(f'Square Moment: {moment}\nSquare Mass: {mass}')
        square.addToSpace()
        pass

    def createRagdollV1(self):
        dummy = RagdollV1(self.parent.space, self.parent.body.position)
        dummy.addToSpace()

    def createRagdollV2(self):
        dummy = RagdollV2(self.parent.space, self.parent.body.position)
        dummy.addToSpace()

    def createRagdollV3(self):
        dummy = RagdollV3(self.parent.space, self.parent.body.position)
        dummy.addToSpace()

    def createRagdollV4(self):
        dummy = RagdollV4(self.parent.space, self.parent.body.position)
        dummy.addToSpace()



class grabTool:
    def __init__(self, parent):
        self.parent = parent
        self.joint = None
        pass

    def create_joint(self, space, shape, nearest):
        self.joint = pymunk.PivotJoint(self.parent.body, shape.body, (0, 0), shape.body.world_to_local(nearest))
        self.joint.max_bias = 50000
        self.joint.max_force = 20 ** 60
        space.add(self.joint)

    def detect_joint(self, event):
        p = (event.pos[0] - self.parent.offset_vector[0] - self.parent.camera_offset[0], event.pos[1] - self.parent.offset_vector[1] - self.parent.camera_offset[1])
        hit = self.parent.space.point_query_nearest(p, self.parent.radius, pymunk.ShapeFilter())
        if hit is not None and hit.shape.body.body_type == pymunk.Body.DYNAMIC:
            shape = hit.shape
            if hit.distance > 0:
                nearest = hit.point
            else:
                nearest = p

            self.create_joint(self.parent.space, shape, nearest)

    def reset_joint(self):
        if self.joint is not None:
            self.parent.space.remove(self.joint)
            self.joint = None

    def event_handler(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            self.detect_joint(event)

        if event.type == MOUSEBUTTONUP and event.button == 1:
            self.reset_joint()
