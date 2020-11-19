import math

from Box2D import *
import pygame as pyg

from constants import *
import utils

# Entity is an abstract class
class Entity:
    def __init__(self, world, name):
        self.world = world
        box = (self.width() / 2, self.height() / 2)
        if self.is_static():
            self.body = self.world.engine.CreateStaticBody(
                position=self.init_pos(),
                shapes=b2PolygonShape(box=box),
                )
        else:
            self.body = self.world.engine.CreateDynamicBody(
                position=self.init_pos(),
                shapes=b2PolygonShape(box=box),
                )
        self.body.userData = name

    def draw(self, screen):
        self.custom_draw(screen)
        left_m = self.x() - self.width() / 2
        left_p = left_m * self.world.pixels_per_meter
        top_m = self.y() - self.height() / 2
        top_p = top_m * self.world.pixels_per_meter

        width_p = self.width() * self.world.pixels_per_meter
        height_p = self.height() * self.world.pixels_per_meter
        r = pyg.Rect(left_p, top_p, width_p, height_p)
        width = 0 if self.draw_fill() else 1
        pyg.draw.rect(screen, self.color(), r, width=width)

    def custom_draw(self, screen):
        pass

    def is_static(self):
        return True

    def draw_fill(self):
        return True

    # meters
    def x(self):
        return self.body.position.x

    # meters
    def y(self):
        return self.body.position.y

class Wall(Entity):
    def __init__(self, world, name, x, y, width, height):
        self.position = (x, y)
        self.w = width
        self.h = height
        super().__init__(world, name)

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
        return GREY

class Goal(Wall):
    def color(self):
        return BLUE

class Player(Entity):
    def __init__(self, world, name, x, y, width, height):
        self.init_position = (x, y)
        self.w = width
        self.h = height
        super().__init__(world, name)

    def is_static(self):
        return False

    # meters
    def init_pos(self):
        return self.init_position

    # meters
    def width(self):
        return self.w

    # meters
    def height(self):
        return self.h

    def color(self):
        return WHITE

    def step(self, keys):
        if self.touch_goal():
            return True
        if pyg.K_a in keys:
            force = b2Vec2(-1, 0)
            self.body.ApplyForceToCenter(force, wake=True)
        if pyg.K_d in keys:
            force = b2Vec2(1, 0)
            self.body.ApplyForceToCenter(force, wake=True)
        if pyg.K_SPACE in keys and self.can_jump():
            impulse = b2Vec2(0, -1.5)
            self.body.ApplyLinearImpulse(impulse, self.body.worldCenter, wake=True)

        vel = self.body.linearVelocity
        speed = vel.length
        drag = DRAG_COEFF * speed * -vel
        self.body.ApplyForceToCenter(drag, wake=True)
        return False
    
    def can_jump(self):
        for edge in self.body.contacts:
            c = edge.contact
            if c.touching:
                # Box2D convention: the normal points from fixtureA to fixtureB.
                if c.fixtureA.body == self.body:
                    nominal_vector = b2Vec2(0, 1)
                elif c.fixtureB.body == self.body:
                    nominal_vector = b2Vec2(0, -1)
                else:
                    raise Exception("WTF?")

                if utils.vectors_close(c.worldManifold.normal, nominal_vector):
                    return True
        return False

    def touch_goal(self):
        for edge in self.body.contacts:
            c = edge.contact
            if c.touching and edge.other.userData == "goal":
                print("YOU WIN")
                return True
        return False

    def custom_draw(self, screen):
        '''
        Draw the flashlight from the player to the first object hit.
        Do this with many rays. Use the physics engine to find the end of each ray.
        '''
        light_half_deg = 15
        light_half_rad = light_half_deg * math.pi / 180
        light_step_deg = 0.4
        light_step_rad = light_step_deg * math.pi / 180

        for delta_angle in utils.float_range(-light_half_rad, light_half_rad, light_step_rad):
            # gather necessary data
            player_x_p = self.x() * self.world.pixels_per_meter
            player_y_p = self.y() * self.world.pixels_per_meter
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
            player_pos_m = (player_pos_p[0] * self.world.meters_per_pixel, player_pos_p[1] * self.world.meters_per_pixel)
            ray_dir_m = (ray_dir[0] * self.world.meters_per_pixel, ray_dir[1] * self.world.meters_per_pixel)
            self.world.engine.RayCast(ray, player_pos_m, ray_dir_m)
            if ray.end_point_m == None:
                # Didn't hit anything. Draw to end of screen
                ray_end_p = ray_dir
            else:
                # Hit something. Stop drawing ray there
                ray_end_p = (ray.end_point_m[0] * self.world.pixels_per_meter, ray.end_point_m[1] * self.world.pixels_per_meter)

            # draw
            pyg.draw.line(screen, YELLOW, player_pos_p, ray_end_p)
        return False

    def draw_fill(self):
        return False
