import argparse
import sys
import time

import pygame as pyg

from constants import *
from world import World
from editor import Editor

def screen_size(args):
    w = SCREEN_WIDTH
    h = SCREEN_HEIGHT
    if args.map_editor:
        w += EDITOR_BORDER * 2
        h += EDITOR_BORDER * 2
    return (w, h)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--map-editor", help="launch editor for building maps", action="store_true")
    parser.add_argument("--debug", help="turn on the lights", action="store_true")
    parser.add_argument("--map-file", help="a json file that specifies a map", required=True)
    args = parser.parse_args()

    # IO engine
    pyg.init()

    editor = None
    if args.map_editor:
        editor = Editor(args)
    world = World(args)
    screen = pyg.display.set_mode(screen_size(args))

    prev_time_s = time.time()
    keys = set()
    while True:
        # take input
        events = []
        for event in pyg.event.get():
            events.append(event)
            if event.type == pyg.QUIT:
                return
            elif event.type == pyg.KEYDOWN:
                keys.add(event.key)
            elif event.type == pyg.KEYUP:
                keys.discard(event.key)

        # simulate
        if editor != None:
            should_reload = editor.handle(events, screen)
            if should_reload:
                world = World(args)
        if world.step(keys):
            return

        # draw
        screen.fill(BLACK)
        world.draw(screen)
        if editor != None:
            editor.draw(screen)
        pyg.display.flip()

        # sleep
        cur_time_s = time.time()
        elapsed_s = cur_time_s - prev_time_s
        wait_s = TIME_STEP_S - elapsed_s
        if wait_s >= 0.0:
            time.sleep(wait_s)
        prev_time_s = cur_time_s
                   
if __name__ == "__main__":
    main()