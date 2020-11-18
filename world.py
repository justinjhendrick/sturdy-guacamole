import json
import pygame as pyg
from Box2D import *

from constants import *
from entity import Player, Wall, Goal

class World:

    def __init__(self, args):
        self.args = args
        self.engine = b2World(gravity=(0, GRAVITY))
        self.player = Player(self.engine)
        self.load_map_file()

    def load_map_file(self):
        self.goals = []
        self.statics = []
        with open(self.args.map_file) as f:
            top = json.loads(f.read())
            statics = top['statics']
            for static in statics:
                t = static['type']
                name = static['name']
                if t == "wall":
                    x = static['x_center']
                    y = static['y_center']
                    w = static['w_half']
                    h = static['h_half']
                    if name == "goal":
                        wall = Goal(self.engine, x, y, w, h, name)
                        self.goals.append(wall)
                    else:
                        wall = Wall(self.engine, x, y, w, h, name)
                    self.statics.append(wall)
                else:
                    raise Exception("Unexpected static type {}".format(t))
            
    
    def step(self, keys):
        if self.player.step(keys):
            return True

        vel_iters = 6
        pos_iters = 2
        self.engine.Step(TIME_STEP_S, vel_iters, pos_iters)
        self.engine.ClearForces()

    def draw(self, screen):
        if self.args.debug:
            for static in self.statics:
                static.draw(screen)
        else:
            for goal in self.goals:
                goal.draw(screen)
        self.player.draw(screen)