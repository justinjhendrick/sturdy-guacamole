import os
from enum import Enum
import json
import pygame as pyg

from constants import *

class Mode(Enum):
    NONE = 0,
    RECT = 1,

class Rect():
    def __init__(self, editor):
        self.editor = editor
        self.reset()

    def reset(self):
        self.active = False
        self.corners = []

    def enter(self):
        self.active = True

    def handle(self, event):
        if self.active:
            if event.type == pyg.MOUSEBUTTONDOWN:
                assert(len(self.corners) == 0)
                self.corners.append(event.pos)
            elif event.type == pyg.MOUSEBUTTONUP:
                assert(len(self.corners) == 1)
                self.corners.append(event.pos)

    def exit(self):
        result = None
        if self.active and len(self.corners) == 2:
            x0 = self.editor.to_meters(self.corners[0][0])
            x1 = self.editor.to_meters(self.corners[1][0])
            y0 = self.editor.to_meters(self.corners[0][1])
            y1 = self.editor.to_meters(self.corners[1][1])
            width = abs(x0 - x1)
            height = abs(y0 - y1)
            left = min(x0, x1)
            top = min(y0, y1)
            result = {}
            result['name'] = 'wall'
            result['type'] = 'wall'
            result['x_center'] = left + width / 2
            result['y_center'] = top + height / 2
            result['w_half'] = width / 2
            result['h_half'] = height / 2
        self.reset()
        return result

class Editor:
    def __init__(self, args):
        self.args = args
        self.triggers = {
            pyg.K_r: Rect(self),
        }
        if os.path.isfile(self.args.map_file):
            with open(self.args.map_file, mode='r') as f:
                self.map = json.loads(f.read())
        else:
            self.map = {}
            self.map['width'] = 32
            self.map['name'] = self.args.map_file.strip().split('./_')[-3]
        self._pixels_per_meter = SCREEN_WIDTH / self.map['width']
        self._meters_per_pixel = 1.0 / self._pixels_per_meter

    def handle(self, event, screen):
        should_reload = False
        if event.type == pyg.KEYDOWN:
            if event.key in self.triggers.keys():
                self.triggers[event.key].enter()
        if event.type == pyg.KEYUP:
            if event.key in self.triggers.keys():
                result = self.triggers[event.key].exit()
                if result != None:
                    self.map['statics'].append(result)
                    should_reload = True
        for _, v in self.triggers.items():
            v.handle(event)
        if should_reload:
            with open(self.args.map_file, mode='w') as f:
                json.dump(self.map, f, indent=2)
        return should_reload

    def to_meters(self, pixels, is_position=True):
        if is_position:
            pixels -= EDITOR_BORDER
        meters = pixels * self._meters_per_pixel
        return meters 

    def to_pixels(self, meters, is_position=True):
        pixels = meters * self._pixels_per_meter
        if is_position:
            pixels += EDITOR_BORDER
        return pixels