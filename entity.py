import math

from Box2D import *
import pygame as pyg

from constants import *
from utils import float_range

# Entity is an abstract class
class Entity:
    def __init__(self, engine):
        self.engine = engine
        box = (self.width() / 2, self.height() / 2)
        if self.is_static():
            self.body = engine.CreateStaticBody(
                position=self.init_pos(),
                shapes=b2PolygonShape(box=box),
                )
        else:
            self.body = engine.CreateDynamicBody(
                position=self.init_pos(),
                shapes=b2PolygonShape(box=box),
                )

    def draw(self, screen):
        if self.custom_draw(screen):
            return
        left_m = self.x() - self.width() / 2
        left_p = left_m * PIXELS_PER_METER
        top_m = self.y() - self.height() / 2
        top_p = top_m * PIXELS_PER_METER

        width_p = self.width() * PIXELS_PER_METER
        height_p = self.height() * PIXELS_PER_METER
        r = pyg.Rect(left_p, top_p, width_p, height_p)
        pyg.draw.rect(screen, self.color(), r)

    # meters
    def x(self):
        return self.body.position.x

    # meters
    def y(self):
        return self.body.position.y

class Wall(Entity):
    def __init__(self, engine, x, y, width, height):
        self.position = (x, y)
        self.w = width
        self.h = height
        super().__init__(engine)

    def is_static(self):
        return True

    # meters
    def init_pos(self):
        return self.position

    # meters
    def width(self):
        return self.w

    # meters
    def height(self):
        return self.h

    def color(self):
        return BLACK

    def custom_draw(self, screen):
        return False

class Player(Entity):
    def is_static(self):
        return False

    # meters
    def init_pos(self):
        x_m = (SCREEN_WIDTH * METERS_PER_PIXEL) / 2.0
        return x_m, self.height() / 2

    # meters
    def width(self):
        return 1

    # meters
    def height(self):
        return 1

    def color(self):
        return WHITE

    def step(self, keys):
        if pyg.K_a in keys:
            force = b2Vec2(-1, 0)
            self.body.ApplyForceToCenter(force, wake=True)
        if pyg.K_d in keys:
            force = b2Vec2(1, 0)
            self.body.ApplyForceToCenter(force, wake=True)
        if pyg.K_SPACE in keys:
            force = b2Vec2(0, -4)
            self.body.ApplyForceToCenter(force, wake=True)

        vel = self.body.linearVelocity
        speed = vel.length
        drag = DRAG_COEFF * speed * -vel
        self.body.ApplyForceToCenter(drag, wake=True)

    def custom_draw(self, screen):
        '''
        Draw the flashlight from the player to the first object hit.
        Do this with many rays
        '''
        light_half_deg = 15
        light_half_rad = light_half_deg * math.pi / 180
        light_density_deg = 0.5
        light_density_rad = light_density_deg * math.pi / 180

        for delta_angle in float_range(-light_half_rad, light_half_rad, light_density_rad):
            # gather necessary data
            player_x_p = self.x() * PIXELS_PER_METER
            player_y_p = self.y() * PIXELS_PER_METER
            player_pos_p = (player_x_p, player_y_p)
            mouse_pos_p = pyg.mouse.get_pos()
            mouse_x_p = mouse_pos_p[0]
            mouse_y_p = mouse_pos_p[1]

            # compute ray direction
            ray_length_p = math.hypot(SCREEN_WIDTH, SCREEN_HEIGHT) # longest possible
            center_angle = math.atan2(mouse_y_p - player_y_p, mouse_x_p - player_x_p)
            ray_angle = center_angle + delta_angle
            ray_dir_delta_y_p = ray_length_p * math.sin(ray_angle)
            ray_dir_delta_x_p = ray_length_p * math.cos(ray_angle)
            ray_dir = (player_x_p + ray_dir_delta_x_p, player_y_p + ray_dir_delta_y_p)

            # cast the ray and see what we hit
            class RayCastCallback:
                    def __init__(self, **kwargs):
                        b2RayCastCallback.__init__(self)
                        self.end_point_m = None
                    def ReportFixture(self, fixture, point, normal, fraction):
                        self.end_point_m = b2Vec2(point)
                        return fraction

            ray = RayCastCallback()
            player_pos_m = (player_pos_p[0] * METERS_PER_PIXEL, player_pos_p[1] * METERS_PER_PIXEL)
            ray_dir_m = (ray_dir[0] * METERS_PER_PIXEL, ray_dir[1] * METERS_PER_PIXEL)
            self.engine.RayCast(ray, player_pos_m, ray_dir_m)
            if ray.end_point_m == None:
                # Didn't hit anything. Draw to end of screen
                ray_end_p = ray_dir
            else:
                # Hit something. Stop drawing ray there
                ray_end_p = (ray.end_point_m[0] * PIXELS_PER_METER, ray.end_point_m[1] * PIXELS_PER_METER)

            # draw
            pyg.draw.line(screen, YELLOW, player_pos_p, ray_end_p)
        return True
