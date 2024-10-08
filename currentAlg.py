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

def remove_random_Ls(grid, lightmap, num_to_remove=5):
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
        lightmap[i][j] = None
    
    return grid

def generate_neighbor(map, lightmap):
    """Generate a neighboring state by removing and adding lights."""
    new_map = copy.deepcopy(map)
    new_lightmap = copy.deepcopy(lightmap)
    # Remove 5 random lights
    new_map = remove_random_Ls(new_map, new_lightmap)
    validate_board(new_map, get_locations(lightmap))
    return new_map


def simulated_annealing(init_grid, T_initial, T_final, alpha, lightmap):
    current_state = init_grid
    current_energy = determine_violations(current_state)
    T = T_initial

    while T > T_final:
        for _ in range(100):  # Number of iterations at each temperature
            neighbor = generate_neighbor(current_state, lightmap)
            neighbor_energy = determine_violations(neighbor)

            # Acceptance criteria
            if neighbor_energy < current_energy:  # If it's better, accept it
                current_state = neighbor
                current_energy = neighbor_energy
            else:
                # Calculate acceptance probability
                acceptance_probability = np.exp((current_energy - neighbor_energy) / T)
                if random.random() < acceptance_probability:
                    current_state = neighbor
                    current_energy = neighbor_energy

        T *= alpha  # Cool down

    return current_state

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

    violations_holder = []
    init_grid = []
    rand_int = random.randint(1,10)
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
        violations_holder.append(violations)

        if i + 1 == rand_int:
            init_grid = map
    print("BRUH")
    print(violations_holder)
    final_state = simulated_annealing(init_grid, 100, 1, 0.95, lightmap)
    with open("test.txt", 'w') as file:
        file.write(str(determine_violations(final_state)) + '\n')
        for row in final_state:
            row_to_write = ''.join(row)
            file.write(row_to_write + '\n')
    
    

    


if __name__ == "__main__":
    main()