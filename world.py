import json
import pygame as pyg
from Box2D import *

from constants import *
from entity import Player, Wall, Goal

class World:
    def __init__(self, args):
        self.args = args
        self.engine = b2World(gravity=(0, GRAVITY))
        self.load_map_file()

    def load_map_file(self):
        '''
        Maps are specified by a json file. Load the map into the physics engine
        '''
        self.dynamics = []
        self.goals = []
        self.statics = []
        with open(self.args.map_file, mode='r') as f:
            top = json.loads(f.read())
            width_m = top['width']
            self._pixels_per_meter = SCREEN_WIDTH / width_m
            self._meters_per_pixel = 1.0 / self._pixels_per_meter
            dynamics = top['dynamics']
            for dynamic in dynamics:
                name = dynamic['name']
                t = dynamic['type']
                if t == "player":
                    x = dynamic['x_center']
                    y = dynamic['y_center']
                    w = dynamic['w_half']
                    h = dynamic['h_half']
                    p = Player(self, name, x, y, w, h)
                    self.player = p
                    self.dynamics.append(p)
                else:
                    raise Exception("Unexpected dynamic type {}".format(t))

            statics = top['statics']
            for static in statics:
                name = static['name']
                t = static['type']
                if t == "wall":
                    x = static['x_center']
                    y = static['y_center']
                    w = static['w_half']
                    h = static['h_half']
                    if name == "goal":
                        wall = Goal(self, name, x, y, w, h)
                        self.goals.append(wall)
                    else:
                        wall = Wall(self, name, x, y, w, h)
                    self.statics.append(wall)
                else:
                    raise Exception("Unexpected static type {}".format(t))
            
    
    def step(self, keys):
        '''
        Run the game for one time step. Returns True if the player wins.
        '''
        if self.player.step(keys):
            return True

        vel_iters = 6
        pos_iters = 2
        self.engine.Step(TIME_STEP_S, vel_iters, pos_iters)
        self.engine.ClearForces()
        return False

    def draw(self, screen):
        '''
        Draw the world and its contents to the screen
        '''
        if self.args.debug:
            for static in self.statics:
                if static.body.userData != "goal":
                    static.draw(screen)
            for dynamic in self.dynamics:
                if dynamic != self.player:
                    dynamic.draw(screen)
        for goal in self.goals:
            goal.draw(screen)
        self.player.draw(screen)

    def to_meters(self, pixels, is_position=True):
        if is_position and self.args.map_editor:
            pixels -= EDITOR_BORDER
        meters = pixels * self._meters_per_pixel
        return meters 

    def to_pixels(self, meters, is_position=True):
        pixels = meters * self._pixels_per_meter
        if is_position and self.args.map_editor:
            pixels += EDITOR_BORDER
        return pixels