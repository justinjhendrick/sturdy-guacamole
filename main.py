import sys
import time

import pygame as pyg

from constants import *
from world import World

def main():
    # IO engine
    pyg.init()

    world = World()
    screen = pyg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    prev_time_s = time.time()
    keys = set()
    while True:
        # take input
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                return
            elif event.type == pyg.KEYDOWN:
                keys.add(event.key)
            elif event.type == pyg.KEYUP:
                keys.discard(event.key)

        # simulate
        if world.step(keys):
            return

        # draw
        screen.fill(BLACK)
        world.draw(screen)
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