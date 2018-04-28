import sys
import math
import random
import time
import threading
from collections import deque

TICKS_PER_SEC = 60

# Size of sectors used to ease block loading.
SECTOR_SIZE = 16

WALKING_SPEED = 5
FLYING_SPEED = 15

GRAVITY = 20.0
MAX_JUMP_HEIGHT = 1.0 # About the height of a block.
# To derive the formula for calculating jump speed, first solve
#    v_t = v_0 + a * t
# for the time at which you achieve maximum height, where a is the acceleration
# due to gravity and v_t = 0. This gives:
#    t = - v_0 / a
# Use t and the desired MAX_JUMP_HEIGHT to solve for v_0 (jump speed) in
#    s = s_0 + v_0 * t + (a * t^2) / 2
JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 50

PLAYER_HEIGHT = 2

FEATURES = dict()


# multi-threading for timer of power_time
class RepeatEvery(threading.Thread):
    def __init__(self, object , window_object):

        threading.Thread.__init__(self)
        self.object =object  # seconds between calls
        self.window_object = window_object
        self.runable = True

    def run(self):
        #global score # make score global for this thread context
        self.object.power_time= 5
        while self.object.power_time > 0 and self.runable:
            time.sleep(1)

            self.object.power_time = self.object.power_time - 1
        self.window_object.flying=False

    def stop(self):
        self.runable = False

###################################################


def cube_vertices(x, y, z, n):
    """ Return the vertices of the cube at position x, y, z with size 2*n.

    """
    return [
        x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # top
        x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
        x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # left
        x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # right
        x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # front
        x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # back
    ]

def square_vertices(t,n):
    x=t[0]
    y=t[1]
    z=t[2]
    return [x,y,z, x+n,y,z, x+n,y+n,z, x,y+n,z]

def tex_coord(x, y, n=16):
    """ Return the bounding vertices of the texture square.

    """
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


def tex_coords(top, bottom, side):
    """ Return a list of the texture squares for the top, bottom and side.

    """
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result



def tex_coords2(top, bottom, side1,side2,side3,side4):
    """ Return a list of the texture squares for the top, bottom and side.
    """
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side1 = tex_coord(*side1)
    side2 = tex_coord(*side2)
    side3 = tex_coord(*side3)
    side4 = tex_coord(*side4)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side1)
    result.extend(side2)
    result.extend(side3)
    result.extend(side4)
    return result

arr =  tex_coords2((6,9),(8,8), (6,8), (7,8),(6,8),(6,8))
#arr = tex_coords2((1,2),(1,0),(0,1),(1,1),(2,1),(3,1))

TEXTURE_PATH = "assets/texture.png"

GRASS1 = tex_coords((1, 6), (2, 15), (3, 15))
GRASS = tex_coords((1, 6), (2, 15), (3, 15))
GRASS2 = tex_coords((2, 6), (2, 15), (3, 15))
ROAD = tex_coords((0, 15), (0, 15), (3, 14))
WALL1 = tex_coords((5, 15), (5, 15), (5, 15))
WALL2 = tex_coords((0, 14), (0, 14), (0, 14))
WALL3 = tex_coords((7, 15), (7, 15), (7, 15))
WALL4 = tex_coords((0,3),(0,1),(0,2))
FLOOR1 = tex_coords((7,14), (3,11), (2,0))
FLOOR2 = tex_coords((6,14), (2,5), (2,0))
FLOOR3 = tex_coords((8,14), (2,4), (2,0))
FLOOR4 = tex_coords((14,12), (3,0), (3,11))
STONE = tex_coords((9, 0), (9, 0), (9, 0))
NOR = tex_coords((1,1),(1,1),(1,1))
FLOW1 = tex_coords((5,11),(1,1),(15,10))
FLOW2 = tex_coords((5,11),(1,1),(6,11))
TOWER = tex_coords2((1,11),(9,14),(9,15),(10,15),(9,15),(10,15))
TOWER2 = tex_coords2((1,12),(9,14),(3,13),(3,13),(3,13),(3,13))



SAND = tex_coords((1, 1), (1, 1), (1, 1))
BRICK = tex_coords((2, 0), (2, 0), (2, 0))
RSTONE = tex_coords((0,3), (0,3), (0,3))
SNOW = tex_coords((3,3), (3,2), (3,2))
MARBLE = tex_coords((3,1), (3,1), (3,1))
ALGAE = tex_coords((2,3), (2,3), (2,3))
COIN = tex_coords((3,0),(3,0),(3,0))
CEMENT = tex_coords((1,2), (1,2), (1,2))

FACES = [
    ( 0, 1, 0),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 0, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]


def normalize(position):
    """ Accepts `position` of arbitrary precision and returns the block
    containing that position.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    block_position : tuple of ints of len 3

    """
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return (x, y, z)



def sectorize(position):
    """ Returns a tuple representing the sector for the given `position`.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    sector : tuple of len 3

    """
    x, y, z = normalize(position)
    x, y, z = x // SECTOR_SIZE, y // SECTOR_SIZE, z // SECTOR_SIZE
    return (x, 0, z)
