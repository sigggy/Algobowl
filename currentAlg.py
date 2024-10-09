# flake8: noqa
import numpy as np
from output_verifier import *
from bowl import write_output, light_bulbs
import copy
from test import *
import random
from graphCreation import *
from printer import *
from betterGreedy import *
import random
import numpy as np

def remove_random_Ls(grid, num_to_remove=5):
    # Get all positions of "L" in the grid
    positions = [(i, j) for i in range(len(grid)) for j in range(len(grid[i])) if grid[i][j] == "L"]
    
    # Randomly select up to `num_to_remove` positions to change
    if len(positions) < num_to_remove:
        print(f"Warning: Not enough 'L's to remove. Attempting to remove {num_to_remove}, but found only {len(positions)}.")
        num_to_remove = len(positions)  # Adjust to the maximum available "L"s
    
    # Randomly sample the positions to change
    positions_to_remove = random.sample(positions, num_to_remove)
    
    # Replace "L" with "."
    for i, j in positions_to_remove:
        grid[i][j] = "."
    
    return grid

def generate_neighbor(light):
    before_config = light.get_curr_config()
    before = light.get_vio_for_light()
    after_config = light.alter_config()
    after = light.get_vio_for_light()

    return after - before, after_config, before_config


def simulated_annealing(violations, num_list, T_initial, T_final, alpha):    
    T = T_initial

    while T > T_final:
        best_light = (None, None)
        best_neighbor_energy = 0
        for _ in range(1000):  # Number of iterations at each temperature step
            random_num = random.choice(num_list)
            neighbor_energy, after_config, before_config = generate_neighbor(random_num)

            # Always take the lowest energy state (strict improvement)
            if neighbor_energy < best_neighbor_energy:  # If neighbor is better, update the best state
                best_light = (random_num, after_config)
                best_energy = neighbor_energy
            # TODO  Not sure if this is right 
            random_num.configure(before_config)
        
        if best_light[0]:
            # TODO Not sure if this is right 
            best_light[0].configure(best_light[1])

        T *= alpha  # Continue cooling down (optional since you're only taking best solutions)


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
    return notimportant, important 


def main():
    _, retMap = get_input_data(sys.argv[1]) # read input

    
    # create graph
    lightmap = [[None for _ in range(len(retMap[0]))] for _ in range(len(retMap))]
    nummap = [[None for _ in range(len(retMap[0]))] for _ in range(len(retMap))]
    map = find_important_squares(retMap, lightmap, nummap)
    num_list = find_collisions(retMap, map, nummap, lightmap)

    num_list_greedy = get_nums(nummap) # get sorted list of nums

    simple_greedy(num_list_greedy)

    # for num in num_list: # get random configs to start
    #     num.alter_config()

    update_map(lightmap, map)

    violations = determine_violations(map)
    print(f'Violations before annealing {violations}')
    simulated_annealing(violations, num_list, T_initial=100, T_final=1, alpha=0.95)

    update_map(lightmap, map)

    for line in map:
        print("".join(line))

    validate_board(map, get_locations(lightmap))

    write_output(map, violations)
    
    print(f'Violations after annealing {violations}')

    violations = determine_violations(map)
    print(f'Violations at the very end {violations}')


    write_output(map, violations)

if __name__ == "__main__":
    main()