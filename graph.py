# flake8: noqa
from output_verifier import *
from bowl import write_output, light_bulbs
import numpy as np
import random

class number_tile:
    def __init__(self, x_pos, y_pos, num):
        self.num = int(num)
        self.i = x_pos
        self.j = y_pos
        self.adjacent_lights = []
        self.configs = []

    def get_lit_lights(self):
        return [light for light in self.adjacent_lights if light.is_lit]

    def mark_num_finished(self): # unlight all lights and mark them as unimportant if not needed by another num
        for light in self.adjacent_lights:
            if light.necesarry == []:
                light.is_lit = False
                light.is_important = False
    
    def get_num_lit_lights(self):
        return len(self.get_lit_lights)

    def pop_nums(self, lit_lights):
        random.shuffle(lit_lights) # possible diff solutions for big boards
        needed_lights = [light for light in lit_lights if light.necesarry != []] # find all needed lights
        
        if len(needed_lights) >= self.num: # if we need all the lights
            for light in lit_lights:
                if light.necesarry == []:
                    light.is_lit = False
            if len(needed_lights) > self.num:
                self.mark_num_finished() # mark num as impossible if too many needed lights
            return
        
        kept_lights = []
        for light in lit_lights: # search for lights we can keep that won't mess up necesarry lights
            if not light.is_neigh_necesarry() and len(kept_lights) != self.num: 
                kept_lights.append(light)
            else:
                light.is_lit = False # unlight light we don't take
        
        if len(kept_lights) != self.num:
            self.mark_num_finished() # give up on num
        for light in kept_lights:
            light.set_light(self)

    def manage_num(self):
        lit_lights = self.get_lit_lights()
        if len(lit_lights) < self.num: # accept light can't be marked
            self.mark_num_finished()
        elif len(lit_lights) == self.num: # mark all lights as set
            for light in lit_lights:
                light.set_light(self)
        else: # find lights to keep, if not enough lights to keep then give up on num
            self.pop_nums(lit_lights)

    def __str__(self) -> str:
        return f'{self.i}, {self.j}'


class number_tile_light:
    def __init__(self, is_lit, i, j):
        self.i = i
        self.j = j
        self.is_lit = is_lit
        self.is_important = True
        self.neighbors = []
        self.necesarry = []

        # TODO need to make a pointer to the number a light is adjcant to so I can remove teh light from it 
        # TODO If you want a number_tile_light to be able to remove itself from multiple number_tile objects that it is adjacent to, you need to create a way to track the relationship between each number_tile_light and all the number_tile objects it is adjacent to.

    def is_neigh_necesarry(self): # return if any nieghbors of light are necesarry
        for light in self.neighbors:
            if light.necesarry != []:
                return True # return true if a neighbor is needed
        return False # return false if no neighbors needed

    def set_light(self, num_light): # unlights all neighbors and marks as important to a num_light
        for light in self.neighbors:
            light.is_lit = False
        self.necesarry.append(num_light) # add num to a necesarry list
    
    def __str__(self) -> str:
        return f"({self.i}, {self.j})"