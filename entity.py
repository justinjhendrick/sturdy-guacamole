from Box2D import *
import pygame as pyg

from constants import *

# Entity is an abstract class
class Entity:
    def __init__(self, engine):
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

class Wall(Entity):
    def is_static(self):
        return True

    # meters
    def init_pos(self):
        x_m = (SCREEN_WIDTH * METERS_PER_PIXEL) / 2.0
        y_m = (SCREEN_HEIGHT * METERS_PER_PIXEL) - (self.height() / 2.0)
        return (x_m, y_m)

    # meters
    def width(self):
        return SCREEN_WIDTH * METERS_PER_PIXEL

    # meters
    def height(self):
        return 10 * METERS_PER_PIXEL

    def color(self):
        return GREY