import pygame as pyg
from Box2D import *

from constants import *
from entity import Player, Wall, Goal

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
        self.platforms = []
        for i in range(0, 5):
            self.platforms.append(Wall(
                self.engine,
                x=240 * METERS_PER_PIXEL + i * screen_width_m / 10,
                y=screen_height_m - (60 * METERS_PER_PIXEL + i * screen_height_m / 20),
                width=10 * wall_size_m,
                height=wall_size_m,
            ))
        self.goal = Goal(
            self.engine,
            x=240 * METERS_PER_PIXEL + 4 * screen_width_m / 10,
            y=screen_height_m - (120 * METERS_PER_PIXEL + 4 * screen_height_m / 20),
            width=2 * wall_size_m,
            height=2 * wall_size_m,
        )
    
    def step(self, keys):
        if self.player.step(keys):
            return True

        vel_iters = 6
        pos_iters = 2
        self.engine.Step(TIME_STEP_S, vel_iters, pos_iters)
        self.engine.ClearForces()

    def draw(self, screen):
        #self.ground.draw(screen)
        #self.ceiling.draw(screen)
        #self.left.draw(screen)
        #self.right.draw(screen)
        #for p in self.platforms:
        #    self.platform.draw(screen)
        self.player.draw(screen)
        self.goal.draw(screen)