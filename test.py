# flake8: noqa
from output_verifier import *
from bowl import write_output, light_bulbs
import numpy as np
import random

class number_tile:
    def __init__(self,x_pos, y_pos, num):
        self.num = num
        self.i = x_pos
        self.j = y_pos
        self.adjacent_lights = []

    def pop_light(self, ):
        pass
    
    def __str__(self) -> str:
        return f'{self.num}'

class number_tile_light:
    def __init__(self, is_lit, i, j):
        self.i = i
        self.j = j
        self.is_lit = is_lit
        self.neighbors = []
        self.collisions = 0

    def rebalance_light(self, ): 
        pass
    
    def __str__(self) -> str:
        return f"({self.i}, {self.j})"