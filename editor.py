import os
import json
import pygame as pyg

from constants import *
import utils

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
                assert(len(self.corners) % 2 == 0)
                self.corners.append(event.pos)
            elif event.type == pyg.MOUSEBUTTONUP:
                assert(len(self.corners) % 2 == 1)
                self.corners.append(event.pos)

    def exit(self):
        results = []
        if self.active and len(self.corners) >= 2:
            assert(len(self.corners) % 2 == 0)
            for x0, y0, x1, y1 in self.get_corners_m():
                left = min(x0, x1)
                top = min(y0, y1)
                width = abs(x0 - x1)
                height = abs(y0 - y1)
                result = {}
                result['name'] = 'wall'
                result['type'] = 'wall'
                result['x_center'] = left + width / 2
                result['y_center'] = top + height / 2
                result['w_half'] = width / 2
                result['h_half'] = height / 2
                results.append(result)
        self.reset()
        return results

    def get_corners_m(self):
        for x0_p, y0_p, x1_p, y1_p in self.get_corners_p():
            x0_m = self.editor.to_meters(x0_p)
            y0_m = self.editor.to_meters(y0_p)
            x1_m = self.editor.to_meters(x1_p)
            y1_m = self.editor.to_meters(y1_p)
            yield (x0_m, y0_m, x1_m, y1_m)

    def get_corners_p(self):
        for i in range(0, len(self.corners), 2):
            if i + 1 < len(self.corners):
                x0, y0 = self.corners[i]
                x1, y1 = self.corners[i + 1]
                yield (x0, y0, x1, y1)

    def draw_one(self, screen, x0, y0, x1, y1):
        left = min(x0, x1)
        top = min(y0, y1)
        width = abs(x0 - x1)
        height = abs(y0 - y1)
        
        r = pyg.Rect(left, top, width, height)
        pyg.draw.rect(screen, LIGHT_GREY, r)

    def draw(self, screen):
        # draw already created rects in this session
        for x0, y0, x1, y1 in self.get_corners_p():
            self.draw_one(screen, x0, y0, x1, y1)
        # draw a hypothetical rect while the mouse is down
        if len(self.corners) % 2 == 1:
            x0, y0 = self.corners[-1]
            x1, y1 = pyg.mouse.get_pos()
            self.draw_one(screen, x0, y0, x1, y1)
            

class Delete:
    def __init__(self, editor):
        self.editor = editor
        self.reset()

    def reset(self):
        self.active = False

    def enter(self):
        self.active = True

    def handle(self, event):
        if self.active:
            if event.type == pyg.MOUSEBUTTONDOWN:
                to_remove = []
                i = 0
                for static in self.editor.map['statics']:
                    x_center = self.editor.to_pixels(static['x_center'])
                    y_center = self.editor.to_pixels(static['y_center'])
                    w_half = self.editor.to_pixels(static['w_half'], is_position=False)
                    h_half = self.editor.to_pixels(static['h_half'], is_position=False)

                    mouse_x, mouse_y = pyg.mouse.get_pos()
                    inside_x = mouse_x >= x_center - w_half and mouse_x <= x_center + w_half
                    inside_y = mouse_y >= y_center - h_half and mouse_y <= y_center + h_half
                    if inside_x and inside_y:
                        to_remove.append(i)
                    i += 1
                for i in to_remove:
                    del self.editor.map['statics'][i]
                return to_remove != []

    def exit(self):
        self.reset()
        return []

    def draw(self, screen):
        pass

class Editor:
    def __init__(self, args):
        self.args = args
        self.triggers = {
            pyg.K_r: Rect(self),
            pyg.K_x: Delete(self),
        }
        if os.path.isfile(self.args.map_file):
            with open(self.args.map_file, mode='r') as f:
                self.map = json.loads(f.read())
        else:
            self.map = {}
            self.map['width'] = 32
            self.map['name'] = utils.split_any(self.args.map_file.strip(), '._' + os.sep)[-3]
            self.map['statics'] = []
            player = {}
            player['name'] = 'player'
            player['type'] = 'player'
            player['x_center'] = 0
            player['y_center'] = 0
            player['w_half'] = 0.25
            player['h_half'] = 0.25
            self.map['dynamics'] = [player]
            self.write_map()
        self._pixels_per_meter = SCREEN_WIDTH / self.map['width']
        self._meters_per_pixel = 1.0 / self._pixels_per_meter

    def handle_one(self, event, screen):
        '''
        Handle one event. Triggers are active while their respective key is held down
        '''
        should_reload = False
        if event.type == pyg.KEYDOWN:
            if event.key in self.triggers.keys():
                self.triggers[event.key].enter()

        for _, v in self.triggers.items():
            if v.handle(event):
                should_reload = True

        results = []
        if event.type == pyg.KEYUP:
            if event.key in self.triggers.keys():
                results = self.triggers[event.key].exit()
                for result in results:
                    self.map['statics'].append(result)
                    should_reload = True
        return should_reload

    def handle(self, events, screen):
        should_reload = False
        for event in events:
            if self.handle_one(event, screen):
                should_reload = True
        if should_reload:
            self.write_map()
        return should_reload

    def draw(self, screen):
        for _, v in self.triggers.items():
            v.draw(screen)

        # draw playable area border
        r = pyg.Rect(EDITOR_BORDER, EDITOR_BORDER, SCREEN_WIDTH, SCREEN_HEIGHT)
        pyg.draw.rect(screen, WHITE, r, width=1)

    def write_map(self):
        with open(self.args.map_file, mode='w') as f:
            json.dump(self.map, f, indent=2)

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