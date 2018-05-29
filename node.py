from skimage import io
import sys
import math
import numpy

class node:

    def __init__(self, x, y, z):

        self.x = x
        self.y = y
        self.z = z

        self.dis = 0.0

        self.parent = None

        self.radius = 0 # 0.0????????????
