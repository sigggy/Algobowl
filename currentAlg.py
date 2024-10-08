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

def generate_neighbor(retMap):
    """Generate a neighboring state by removing and adding lights."""
    # Remove 5 random lights
    retMap = remove_random_Ls(retMap)
    lightmap = [[None for _ in range(len(retMap[0]))] for _ in range(len(retMap))]
    nummap = [[None for _ in range(len(retMap[0]))] for _ in range(len(retMap))]
    map = find_important_squares(retMap, lightmap, nummap)
    find_collisions(retMap, map, nummap, lightmap)
    num_list = get_nums(nummap) # get sorted list of nums
    simple_greedy(num_list)
    update_map(lightmap, map)
    validate_board(map, get_locations(lightmap)) 
    return map


def simulated_annealing(init_grid, T_initial, T_final, alpha):
    current_state = init_grid
    current_energy = determine_violations(current_state)
    
    # Initialize best state and energy
    best_state = copy.deepcopy(current_state)
    best_energy = current_energy
    
    energies = []
    energies.append(current_energy)
    
    T = T_initial
    
    while T > T_final:
        for _ in range(100):  # Number of iterations at each temperature step
            neighbor = generate_neighbor(current_state)
            neighbor_energy = determine_violations(neighbor)

            # Always take the lowest energy state (strict improvement)
            if neighbor_energy < best_energy:  # If neighbor is better, update the best state
                best_state = neighbor
                best_energy = neighbor_energy
                energies.append(best_energy)

        T *= alpha  # Continue cooling down (optional since you're only taking best solutions)

    print(f"Energy min: {np.min(energies)}")
    return best_state


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
    _, retMap = get_input_data(sys.argv[1]) # read input

    violations_holder = 10000000000
    for i in range(10):
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

        write_output(map, violations)

    # final_state = simulated_annealing(init_grid, 100, 1, 0.95)
    # print(violations_holder)
    # with open("test.txt", 'w') as file:
    #     file.write(str(determine_violations(final_state)) + '\n')
    #     for row in final_state:
    #         row_to_write = ''.join(row)
    #         file.write(row_to_write + '\n')
    
    

    


if __name__ == "__main__":
    main()