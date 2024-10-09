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

def remove_random_Ls(grid, light_map, num_to_remove=2):
    for i in range(len(light_map)):
        for j in range(len(light_map[0])):
            if light_map[i][j]:
                grid[i][j] = 'L'
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

def generate_neighbor(grid, light_map):
    new_grid = copy.deepcopy(grid)
    new_light_map = copy.deepcopy(light_map)

    new_grid = remove_random_Ls(new_grid, new_light_map)
    validate_board(new_grid, get_locations(new_light_map))  

    return new_grid, new_light_map


def simulated_annealing(violations, grid, light_map, T_initial, T_final, alpha):    
    best = grid
    best_map = light_map
    best_eval = violations
    current, current_eval, current_map = best, best_eval, best_map
    T = T_initial
    scores = []

    for i in range(1):
        t = T / float(i + 1)

        candidate, candidate_map = generate_neighbor(current, best_map)
        candidate_eval = determine_violations(candidate)

        if candidate_eval < best_eval or random.random() < math.exp((current_eval - candidate_eval) / t):
            current, current_eval, current_map = candidate, candidate_eval, current_map
            if candidate_eval < best_eval:
                best, best_eval, best_map = candidate, candidate_eval, candidate_map
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

        if violations < best_violations:
            best_violations = violations
            best_map = copy.deepcopy(map)  
            best_light_map = copy.deepcopy(lightmap)  
    before_violations = violations
    
    output_map, output_violations, scores = simulated_annealing(best_violations, best_map, best_light_map, T_initial=100, T_final=1, alpha=0.95)
    print(f' violations before anneal {before_violations}')
    print(f' violations after anneal {violations}')
    write_output(output_map, output_violations)


if __name__ == "__main__":
    main()