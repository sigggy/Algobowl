# flake8: noqa
from output_verifier import *
from bowl import write_output, light_bulbs
import numpy as np
import random

class number_tile:
    def __init__(self,x_pos, y_pos, num):
        self.num = int(num)
        self.i = x_pos
        self.j = y_pos
        self.adjacent_lights = []

    def pop_light(self, ):

        for light in self.adjacent_lights:
            if not light.is_lit:
                print(f' this light is not lit but still adjacent {light}')
                self.adjacent_lights.remove(light)

        if len(self.adjacent_lights) == self.num:
            return 


        if len(self.adjacent_lights) < self.num:
            print(f'num {self} cannot be satisfied')
            for light in self.adjacent_lights:
                print(f"Removed light: {light}")
                light.rebalance_light()
            self.adjacent_lights = []
            
            return
        while len(self.adjacent_lights) > self.num:
            
            max_collisions = max(self.adjacent_lights, key=lambda light: light.collisions).collisions
            max_lights = [light for light in self.adjacent_lights if light.collisions == max_collisions]
            light_to_remove = random.choice(max_lights)

            
            light_to_remove.rebalance_light()
            self.adjacent_lights.remove(light_to_remove)
            print(f"Removed light: {light_to_remove}")

                
    
    def __str__(self) -> str:
        #return f'{self.num} ({self.i},{self.j})'
        return f'{self.num}'


class number_tile_light:
    def __init__(self, is_lit, i, j):
        self.i = i
        self.j = j
        self.is_lit = is_lit
        self.neighbors = []
        self.collisions = 0

        # TODO need to make a pointer to the number a light is adjcant to so I can remove teh light from it 
        # TODO If you want a number_tile_light to be able to remove itself from multiple number_tile objects that it is adjacent to, you need to create a way to track the relationship between each number_tile_light and all the number_tile objects it is adjacent to.
    def rebalance_light(self,): 
        self.is_lit = False 
        for collision in self.neighbors:
            if self in collision.neighbors:
                print(len(collision.neighbors))
                collision.neighbors.remove(self)
                print(f"Removed self ({self.i}, {self.j}) from neighbor ({collision.i}, {collision.j})")
               
                collision.collisions = len(collision.neighbors)
                print(len(collision.neighbors))
                print()
        self.neighbors = []
        print(f"Rebalanced light at ({self.i}, {self.j}) and removed all neighbors.")        
        print()
        print()



    
    def __str__(self) -> str:
        return f"({self.i}, {self.j})"