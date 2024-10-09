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
sys.setrecursionlimit(150000000)

def remove_random_Ls(grid, num_to_remove=2):
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

def add_random_Ls(grid, num_to_add=2):
    # Get all empty positions "." in the grid
    empty_positions = [(i, j) for i in range(len(grid)) for j in range(len(grid[i])) if grid[i][j] == "."]
    
    # Randomly select up to `num_to_add` positions to place "L"
    if len(empty_positions) < num_to_add:
        print(f"Warning: Not enough empty positions to add 'L'. Attempting to add {num_to_add}, but found only {len(empty_positions)}.")
        num_to_add = len(empty_positions)  # Adjust to the maximum available empty positions
    
    # Randomly sample the positions to place "L"
    positions_to_add = random.sample(empty_positions, num_to_add)
    
    # Replace "." with "L"
    for i, j in positions_to_add:
        grid[i][j] = "L"
    
    return grid


def generate_neighbor(grid):
    new_grid = copy.deepcopy(grid)

    new_grid = add_random_Ls(new_grid)  
    new_grid = remove_random_Ls(new_grid)  

    new_light_map = [[None for _ in range(len(new_grid[0]))] for _ in range(len(new_grid))]
    new_nummap = [[None for _ in range(len(new_grid[0]))] for _ in range(len(new_grid))]


    neighbor = find_important_squares(new_grid, new_light_map, new_nummap)  
    num_list = find_collisions(new_grid, neighbor, new_nummap, new_light_map)
    num_list_greedy = get_nums(new_nummap) 
    simple_greedy(num_list_greedy)  
    update_map(new_light_map, neighbor)  
 

    validate_board(neighbor, get_locations(new_light_map)) 
    violations = determine_violations(neighbor)

    return neighbor, violations


def simulated_annealing(violations, grid, T_initial, T_final, alpha):    
    best = grid
    best_eval = violations
    current, current_eval = best, best_eval
    T = T_initial
    scores = [best_eval]

    for i in range(500):
        t = T_initial * (alpha ** i)

        candidate, candidate_eval = generate_neighbor(current)
        scores.append(candidate_eval)
        if candidate_eval < best_eval or random.random() < math.exp((current_eval - candidate_eval) / t):
            current, current_eval = candidate, candidate_eval
            if candidate_eval < best_eval:
                best, best_eval = candidate, candidate_eval
                scores.append(best_eval)

        if i % 10 == 0:
            print(f"Iteration {i}, Temperature {t:.3f}, Best Evaluation {best_eval:.5f}")

    return best, best_eval, scores

   


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


import copy

def main():
    _, retMap = get_input_data(sys.argv[1])  

    best_map = None
    best_violations = float('inf')  
    best_light_map = None
    violations_list = []

    for _ in range(20):
        lightmap = [[None for _ in range(len(retMap[0]))] for _ in range(len(retMap))]
        nummap = [[None for _ in range(len(retMap[0]))] for _ in range(len(retMap))]
        map = find_important_squares(retMap, lightmap, nummap)
        num_list = find_collisions(retMap, map, nummap, lightmap)

        num_list_greedy = get_nums(nummap)  

        simple_greedy(num_list_greedy)  

        update_map(lightmap, map)  

        for line in map:
            print("".join(line))

        validate_board(map, get_locations(lightmap)) 

        violations = determine_violations(map)
        violations_list.append(violations)

        if violations < best_violations:
            best_violations = violations
            best_map = copy.deepcopy(map)  
            best_light_map = copy.deepcopy(lightmap)  
    before_violations = violations
    
    T_initial = np.std(violations_list)
    output_map, output_violations, scores = simulated_annealing(best_violations, best_map, T_initial, T_final=0.5, alpha=0.95)
    print(f' violations before anneal {before_violations}')
    print(f' violations after anneal {violations}')
    print(scores)
    write_output(output_map, output_violations)


if __name__ == "__main__":
    main()