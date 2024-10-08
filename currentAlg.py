import numpy as np
from output_verifier import *
from bowl import write_output, light_bulbs
import copy
from test import *
import random
from graphCreation import *
from printer import *
from betterGreedy import *
import os

def get_nums(nummap):
    nums_list = []
    for i in range(len(nummap)):
        for j in range(len(nummap[0])):
            if nummap[i][j]:
                nums_list.append(nummap[i][j])

    # Sort nums_list by `num` attribute in descending order
    sorted_nums_list = sorted(nums_list, key=lambda x: x.num, reverse=True)
    
    #return sorted_nums_list
    return sorted_nums_list

def simple_greedy(list_nums):
    for num in list_nums:
        num.manage_num()

def get_locations(light_map):
    important = []
    notimportant = []
    for i in range(len(light_map)):
        for j in range(len(light_map[0])):
            if light_map[i][j] and light_map[i][j].is_important:
                important.append((i,j))
            else:
                notimportant.append((i, j))
    random.shuffle(notimportant)
    random.shuffle(important)
    return notimportant + important 


def main():
    input_dir = "actualInputs"
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_dir, filename)
            best_violations = 1000000000
            final_grid = []
            for i in range(10):
                _, retMap = get_input_data(input_file_path) # read input

                # create graph
                lightmap = [[None for _ in range(len(retMap[0]))] for _ in range(len(retMap))]
                nummap = [[None for _ in range(len(retMap[0]))] for _ in range(len(retMap))]
                map = find_important_squares(retMap, lightmap, nummap)
                find_collisions(retMap, map, nummap, lightmap)

                num_list = get_nums(nummap) # get sorted list of nums

                simple_greedy(num_list)

                update_map(lightmap, map)


                violations = determine_violations(map)
                    
                validate_board(map, get_locations(lightmap))

                violations = determine_violations(map)
                if violations < best_violations:
                    best_violations = violations
                    final_grid = map
            
            write_output(final_grid, best_violations, filename)

if __name__ == "__main__":
    main()