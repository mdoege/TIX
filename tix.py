#!/usr/bin/env python

# Displays the TIX clock
# 2011-01-08 / 2020-06-12

# Usage: pytix.py [update interval] [--24]

import pygame

import sys, time, random

try: inter = int(sys.argv[1])
except: inter = 4        # default update interval (secs)

RED = 204, 0, 0
GREEN = 78, 154, 6
BLUE = 52, 101, 164
BACKGROUND = 33, 41, 46
GRAY = 76, 80, 82
COL = (BACKGROUND, BACKGROUND, GRAY, RED, GREEN, BLUE)

if '--24' in sys.argv:
    f = '%H%M'
else:
    f = '%I%M'

def tog(start, end, n, col = 2):
    "Toggle on n values randomly in the array between start and end"
    global disp

    for z in random.sample(range(3 * (end - start)), n):
        disp[z % 3][start + z // 3] = col

def mainprog(win, res):
    global disp

    boxx, boxy = res[0] // 12, res[0] // 12

    t = time.strftime(f, time.localtime())
    h1, h2, m1, m2 = [int(x) for x in t]
    disp = [[2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2] for y in range(3)]
    tog(0, 1, h1, 3)
    tog(2, 5, h2, 4)
    tog(6, 8, m1, 5)
    tog(9, 12, m2, 3)
    for x in range(12):
        for y in range(3):
            pygame.draw.rect(win, COL[disp[y][x]], [x * boxx + 1, y * boxy + 1, boxx - 2, boxy - 2])

class TIX:
    def __init__(self):
        pygame.init()
        self.res = 840, 210
        self.screen = pygame.display.set_mode(self.res, pygame.RESIZABLE)
        pygame.display.set_caption('TIX')
        self.screen.fill(BACKGROUND)
        self.clock = pygame.time.Clock()
        self.last = 0

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.VIDEORESIZE:
                self.res = event.w, event.h
                self.last = 0
                self.screen = pygame.display.set_mode(self.res, pygame.RESIZABLE)

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(1)
            self.events()
            self.update()
        pygame.quit()

    def update(self):
        if time.time() - self.last < inter:
            return
        self.last = time.time()
        self.screen.fill(BACKGROUND)
        mainprog(self.screen, self.res)
        pygame.display.flip()

c = TIX()
c.run()

