import pygame as pyg
from Box2D import *

from constants import *
from entity import Player, Wall

class World:

    def __init__(self):
        self.engine = b2World(gravity=(0, GRAVITY))
        self.player = Player(self.engine)
        self.ground = Wall(self.engine)
    
    def step(self, keys):
        self.player.step(keys)

        vel_iters = 6
        pos_iters = 2
        self.engine.Step(TIME_STEP_S, vel_iters, pos_iters)
        self.engine.ClearForces()

    def draw(self, screen):
        self.ground.draw(screen)
        self.player.draw(screen)