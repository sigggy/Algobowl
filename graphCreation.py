# flake8: noqa
import numpy as np
from output_verifier import *
from bowl import write_output, light_bulbs
import copy
from graph import *
import random
from itertools import permutations

def find_important_squares(board, lightmap, nummap):
    retMap = copy.deepcopy(board)
    
    directions = {
        'left': (0, -1),
        'right': (0, 1),
        'up': (-1, 0),
        'down': (1, 0)
    }

    important_nums = ['0', '1', '2', '3', '4']

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] in important_nums:
                if board[i][j] != '0':
                    nummap[i][j] = number_tile(i, j, board[i][j])
                for direction in directions.values():
                    dr, dc = direction
                    r, c = i + dr, j + dc
                    # Check only one tile over
                    if 0 <= r < len(board) and 0 <= c < len(board[0]):
                        if board[r][c] == '.':
                            retMap[r][c] = '!'
                            if board[i][j] != '0':
                                lightmap[r][c] = number_tile_light(True, r, c)
                            else:
                                lightmap[r][c] = number_tile_light(False, r, c) # if its a 0 start unlit
    return retMap

def find_neighbors_light(retMap, lightmap, i, j):

    important_nums = ['X', '0', '1', '2', '3', '4']

    for x in range(j - 1, -1, -1):
        if retMap[i][x] in important_nums:
            break
        if lightmap[i][x]:
            lightmap[i][j].neighbors.append(lightmap[i][x])
                
    for x in range(j + 1, len(retMap[0])): # check light at location
        if retMap[i][x] in important_nums:
            break
        if lightmap[i][x]:
            lightmap[i][j].neighbors.append(lightmap[i][x])
                
    for y in range(i - 1, -1, -1):
        if retMap[y][j] in important_nums:
            break
        if lightmap[y][j]:
            lightmap[i][j].neighbors.append(lightmap[y][j])
               
    for y in range(i + 1, len(retMap)):
        if retMap[y][j] in important_nums:
            break
        if lightmap[y][j]:
            lightmap[i][j].neighbors.append(lightmap[y][j])

def find_neigh_num(nummap, lightmap, i, j):
    
    directions = {
        'left': (0, -1),
        'right': (0, 1),
        'up': (-1, 0),
        'down': (1, 0)
    }

    adjacent_light_count = 0 

    for direction in directions.values():
        dr, dc = direction
        r, c = i + dr, j + dc
                    # Check only one tile over
        if 0 <= r < len(lightmap) and 0 <= c < len(lightmap[0]):
            if lightmap[r][c]:
                adjacent_light_count += 1
                nummap[i][j].adjacent_lights.append(lightmap[r][c])

    if adjacent_light_count < nummap[i][j].num:
        nummap[i][j].mark_num_finished() # give up on num
    elif adjacent_light_count == nummap[i][j].num:
        for light in nummap[i][j].adjacent_lights:
            light.necesarry.append(nummap[i][j])
 

def find_collisions(board, retMap, nummap, lightmap): # return list of possible nums
    important_nums = ['1', '2', '3', '4']
    nums = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] in important_nums:
                nums.append(nummap[i][j])
                find_neigh_num(nummap, lightmap, i, j)
            if retMap[i][j] == "!":
                find_neighbors_light(board, lightmap, i, j)
    remove_nums = []
    for num in nums:
        if (num.num > len(num.adjacent_lights)):
            remove_nums.append(num)
            continue
        perm_list = [0 for _ in range(len(num.adjacent_lights))]
        for i in range(num.num):
            perm_list[i] = 1
        num.configs = set((permutations(perm_list)))
        num.configs.add(tuple([0 for _ in range(len(num.adjacent_lights))]))
          
    for rem_num in remove_nums: # remove all values that can't be validated
        nums.remove(rem_num)
    return nums

def update_map(lightMap, map):
    for i in range (len(map)):
        for j in range(len(map[0])):
            if lightMap[i][j] and lightMap[i][j].is_lit:
                map[i][j] = 'L'
            if map[i][j] == '!':
                map[i][j] = '.'

if __name__ == "__main__":
    pass