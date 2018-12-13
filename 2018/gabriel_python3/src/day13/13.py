#!/usr/bin/env python3

import os
import copy

try:
    DEBUG=os.environ['DEBUG']
except KeyError:
    DEBUG = None

class Cart(object):
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.distance = 0
        self.next_direction = 'left'

    def turn_right(self):
        if (self.dx, self.dy) == (-1, 0):
            (self.dx, self.dy) = (0, -1)
        elif (self.dx, self.dy) == (1, 0):
            (self.dx, self.dy) = (0, 1)
        elif (self.dx, self.dy) == (0, -1):
            (self.dx, self.dy) = (1, 0)
        elif (self.dx, self.dy) == (0, 1):
            (self.dx, self.dy) = (-1, 0)

    def turn_left(self):
        if (self.dx, self.dy) == (-1, 0):
            (self.dx, self.dy) = (0, 1)
        elif (self.dx, self.dy) == (1, 0):
            (self.dx, self.dy) = (0, -1)
        elif (self.dx, self.dy) == (0, -1):
            (self.dx, self.dy) = (-1, 0)
        elif (self.dx, self.dy) == (0, 1):
            (self.dx, self.dy) = (1, 0)

    def turn(self, current):
        if current == '+':
            if self.next_direction == 'left':
                self.turn_left()
                self.next_direction = 'straight'
            elif self.next_direction == 'straight':
                self.next_direction = 'right'
            else:  # right
                self.turn_right()
                self.next_direction = 'left'

        elif current == '/':
            if self.dx:
                self.turn_left()
            else:
                self.turn_right()
        elif current == '\\':
            if self.dx:
                self.turn_right()
            else:
                self.turn_left()

    def advance(self, current):
        self.turn(current)
        self.x += self.dx
        self.y += self.dy
        self.distance += 1
        return self.x, self.y

    def get_location(self):
        if (self.dx, self.dy) == (-1, 0):
            c = '<'
        elif (self.dx, self.dy) == (1, 0):
            c = '>'
        elif (self.dx, self.dy) == (0, 1):
            c = 'v'
        elif (self.dx, self.dy) == (0, -1):
            c = '^'
        return (self.x, self.y, c)

    def __repr__(self):
        return '{}'.format(self.__dict__)


class Tracks(object):
    def __init__(self, filename):
        self.tracks = list()
        self.carts = set()
        self.ticks = 0

        with open(filename) as f:
            i = 0
            for strline in f:
                line = list(strline[:-1])
                self.tracks.append(line)
                for j in range(len(line)):
                    c = line[j]
                    if c == '<':
                        self.carts.add(Cart(j, i, -1, 0))
                        line[j] = '-'
                    elif c == '>':
                        self.carts.add(Cart(j, i, 1, 0))
                        line[j] = '-'
                    elif c == '^':
                        self.carts.add(Cart(j, i, 0, -1))
                        line[j] = '|'
                    elif c == 'v':
                        self.carts.add(Cart(j, i, 0, 1))
                        line[j] = '|'
                i += 1

    def tick(self):
        self.ticks += 1
        locations = set()
        for cart in self.carts:
            assert self.tracks[cart.y][cart.x] != ' '  # off tracks !!!
            location = cart.advance(self.tracks[cart.y][cart.x])
            if location in locations:
                # crash
                x, y = location
                self.tracks[y][x] = 'X'
                if DEBUG:
                    print(self)
                raise RuntimeError('location: {}'.format(location))
            locations.add(location)

    def __repr__(self):
        tracks = copy.deepcopy(self.tracks)
        for cart in self.carts:
            x, y, c = cart.get_location()
            if tracks[y][x] != 'X':
                tracks[y][x] = c
        rv = ''
        for line in tracks:
            rv += ''.join(line) + '\n'
        return rv


tracks = Tracks('input')
if DEBUG:
    print(tracks)
while True:
    # print(tracks)
    tracks.tick()
