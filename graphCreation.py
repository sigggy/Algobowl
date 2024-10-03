import numpy as np
from output_verifier import *
from bowl import write_output, light_bulbs
import copy
from test import *

def find_important_sqaures(board, lightmap, nummap):
    retMap = copy.deepcopy(board)
    
    directions = {
        'left': (0, -1),
        'right': (0, 1),
        'up': (-1, 0),
        'down': (1, 0)
    }

    important_nums = ['1', '2', '3', '4']

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] in important_nums:
                retMap[i][j] = number_tile(i, j, board[i][j])
                nummap[i][j] = retMap[i][j]
                for direction in directions.values():
                    dr, dc = direction
                    r, c = i + dr, j + dc
                    # Check only one tile over
                    if 0 <= r < len(board) and 0 <= c < len(board[0]):
                        retMap[r][c] = '!'
                        lightmap[r][c] = number_tile_light(True, r, c)
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

def print_grid(grid: List[List[str]]) -> None:
    for row in grid:
        print(" ".join(row))

def find_neigh_num(nummap, lightmap, i, j):
    
    directions = {
        'left': (0, -1),
        'right': (0, 1),
        'up': (-1, 0),
        'down': (1, 0)
    }

    for direction in directions.values():
        dr, dc = direction
        r, c = i + dr, j + dc
                    # Check only one tile over
        if 0 <= r < len(lightmap) and 0 <= c < len(lightmap[0]):
            if lightmap[r][c]:
                nummap[i][j].adjacent_lights.append(lightmap[r][c])

def find_collisions(board, retMap, nummap, lightmap):
    important_nums = ['1', '2', '3', '4']

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] in important_nums:
                find_neigh_num(nummap, lightmap, i, j)
            if retMap[i][j] == "!":
                find_neighbors_light(board, lightmap, i, j)



def main():

    _, retMap = get_input_data(sys.argv[1])
    lightmap = [[None for _ in range(len(retMap[0]))] for _ in range(len(retMap))]
    nummap = [[None for _ in range(len(retMap[0]))] for _ in range(len(retMap))]
    map = find_important_sqaures(retMap, lightmap, nummap)
    find_collisions(retMap, map, nummap, lightmap)


    for i in range(len(lightmap)):
        for j in range(len(lightmap[0])):
            if lightmap[i][j]:
                lightmap[i][j] = lightmap[i][j].__str__()
            print(lightmap[i][j], end = ' ')
        print()

if __name__ == "__main__":
    main()