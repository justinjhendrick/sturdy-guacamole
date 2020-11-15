import pygame as pyg
from Box2D import *

from constants import *
from entity import Player, Wall

class World:

    def __init__(self):
        self.engine = b2World(gravity=(0, GRAVITY))
        self.player = Player(self.engine)
        wall_size_m = 10 * METERS_PER_PIXEL
        screen_width_m = SCREEN_WIDTH * METERS_PER_PIXEL
        screen_height_m = SCREEN_HEIGHT * METERS_PER_PIXEL
        self.ground = Wall(
            self.engine,
            x=screen_width_m / 2,
            y=screen_height_m - wall_size_m / 2,
            width=screen_width_m,
            height=wall_size_m,
        )
        self.ceiling = Wall(
            self.engine,
            x=screen_width_m / 2,
            y=wall_size_m / 2,
            width=screen_width_m,
            height=wall_size_m,
        )
        self.left = Wall(
            self.engine,
            x=wall_size_m / 2,
            y=screen_height_m / 2,
            width=wall_size_m,
            height=screen_height_m,
        )
        self.right = Wall(
            self.engine,
            x=screen_width_m - wall_size_m  / 2,
            y=screen_height_m / 2,
            width=wall_size_m,
            height=screen_height_m,
        )
        self.platform = Wall(
            self.engine,
            x=screen_width_m / 2,
            y=screen_height_m / 2,
            width=10 * wall_size_m,
            height=wall_size_m,
        )
    
    def step(self, keys):
        self.player.step(keys)

        vel_iters = 6
        pos_iters = 2
        self.engine.Step(TIME_STEP_S, vel_iters, pos_iters)
        self.engine.ClearForces()

    def draw(self, screen):
        self.ground.draw(screen)
        self.ceiling.draw(screen)
        self.left.draw(screen)
        self.right.draw(screen)
        self.platform.draw(screen)
        self.player.draw(screen)