# flake8: noqa
import numpy as np
from output_verifier import *
from bowl import write_output, light_bulbs
import copy
from graph import *
import random

def printer(lightmap, nummap, retMap, map):
    for i in range(len(lightmap)):
        for j in range(len(lightmap[0])):
            if lightmap[i][j]:
                print(lightmap[i][j].__str__(), end= ' ')
                continue 
            print(lightmap[i][j], end = ' ')
        print()
    print()

    for i in range(len(lightmap)):
        for j in range(len(lightmap[0])):
            if lightmap[i][j]:
                print(f'light map at {lightmap[i][j].__str__()} with {lightmap[i][j].collisions} collisions')
                for element in lightmap[i][j].neighbors:
                    print(f' -collision at {element.__str__()}')
    
                print()
        print()
        
    for i in range(len(nummap)):
        for j in range(len(nummap[0])):
            if nummap[i][j]:
                print(nummap[i][j].__str__(), end= ' ')
                continue 
            print(nummap[i][j], end = ' ')
        print()
    print()

    for i in range(len(nummap)):
        for j in range(len(nummap[0])):
            if nummap[i][j]:
                print(f'light map at {nummap[i][j].__str__()}')
                for element in nummap[i][j].adjacent_lights:
                    print(f' -adajcent at {element.__str__()}')
    
                print()
        print()

    for i in range (len(retMap)):
        for j in range(len(retMap[0])):
            if retMap[i][j]:
                print(retMap[i][j].__str__(), end= ' ')
                continue 
            print(retMap[i][j], end = ' ')
        print()
    print()

    for i in range (len(map)):
        for j in range(len(map[0])):
            if map[i][j]:
                print(map[i][j].__str__(), end= ' ')
                continue 
            print(map[i][j], end = ' ')
        print()
    print()

def find_important_squares(board, lightmap, nummap):
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
                nummap[i][j] = number_tile(j, i, board[i][j])
                for direction in directions.values():
                    dr, dc = direction
                    r, c = i + dr, j + dc
                    # Check only one tile over
                    if 0 <= r < len(board) and 0 <= c < len(board[0]):
                        if board[r][c] == '.':
                            retMap[r][c] = '!'
                            lightmap[r][c] = number_tile_light(True, c, r)
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
    lightmap[i][j].collisions = len(lightmap[i][j].neighbors)

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

    adjacent_light_count = 0 

    print(f' numx {nummap[i][j]}')
    for direction in directions.values():
        dr, dc = direction
        r, c = i + dr, j + dc
                    # Check only one tile over
        if 0 <= r < len(lightmap) and 0 <= c < len(lightmap[0]):
            if lightmap[r][c]:
                adjacent_light_count += 1
                print(f' lightx {lightmap[r][c]}')
                nummap[i][j].adjacent_lights.append(lightmap[r][c])

    print(f' count {adjacent_light_count} count {len(nummap[i][j].adjacent_lights)}')
    if adjacent_light_count < nummap[i][j].num:
        print(f'This tile is generating invalid lights {nummap[i][j].adjacent_lights}')
        for light in nummap[i][j].adjacent_lights:
            print(f' lighty {light}')
            light.is_valid = False
 

def find_collisions(board, retMap, nummap, lightmap):
    important_nums = ['1', '2', '3', '4']

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] in important_nums:
                find_neigh_num(nummap, lightmap, i, j)
            if retMap[i][j] == "!":
                find_neighbors_light(board, lightmap, i, j)

def get_nums(nummap):
    nums_list = []
    for i in range(len(nummap)):
        for j in range(len(nummap[0])):
            if nummap[i][j]:
                nums_list.append(nummap[i][j])

    # Sort nums_list by `num` attribute in descending order
    sorted_nums_list = sorted(nums_list, key=lambda x: x.num, reverse=True)

    return sorted_nums_list

def update_map(lightMap, map):
    for i in range (len(map)):
        for j in range(len(map[0])):
            if lightMap[i][j] and not lightMap[i][j].is_valid:
                map[i][j] = '.'
                continue 

            if lightMap[i][j] and not lightMap[i][j].is_lit:
                map[i][j] = '.'
                continue 

            if lightMap[i][j]:
                map[i][j] = 'L'

def eliminate_collisions(nummap):
    nums_list = get_nums(nummap)

    for number in nums_list:
        number.pop_light()

def main():

    _, retMap = get_input_data(sys.argv[1])
    lightmap = [[None for _ in range(len(retMap[0]))] for _ in range(len(retMap))]
    nummap = [[None for _ in range(len(retMap[0]))] for _ in range(len(retMap))]
    map = find_important_squares(retMap, lightmap, nummap)
    find_collisions(retMap, map, nummap, lightmap)
    #printer(lightmap, nummap, retMap, map)
    eliminate_collisions(nummap)
    update_map(lightmap, map)
    #printer(lightmap, nummap, retMap, map)
    violations = determine_violations(map)
    write_output(map, violations)

if __name__ == "__main__":
    main()