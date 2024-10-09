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

def generate_neighbor(grid, badLights, GoodLights, num_bad_pops, num_good_pops):
    new_grid = copy.deepcopy(grid)

    new_bad_lights = copy.deepcopy(badLights)
    new_good_lights = copy.deepcopy(GoodLights)

    for _ in range(len(num_bad_pops)):
        light_pop = random.choice(new_bad_lights)
        new_grid[light_pop[light_pop[0]][light_pop[1]]] = '.'
        new_bad_lights.remove(light_pop)
    for _ in range(len(num_good_pops)):
        light_pop = random.choice(new_good_lights)
        new_grid[light_pop[light_pop[0]][light_pop[1]]] = '.'
        new_bad_lights.remove(random.choice(new_good_lights))



    return badLights, GoodLights, new_grid, 



def simulated_annealing(violations, badLights, goodLights, grid, T_initial, T_final, alpha):    
    best = grid
    best_eval = violations
    current, current_eval = best, best_eval
    T = T_initial
    scores = [best_eval]

    for i in range(1):
        t = T_initial / alpha 

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

    update_map(lightmap, map)

    validate_board(map, get_locations(lightmap))

    violations = determine_violations(map)
    print(f'Violations before annealing {violations}')
    simulated_annealing(violations, num_list, T_initial=100, T_final=1, alpha=0.95)

    update_map(lightmap, map)

    validate_board(map, get_locations(lightmap))

    write_output(map, violations)
    
    print(f'Violations after annealing {violations}')

    violations = determine_violations(map)
    print(f'Violations at the very end {violations}')


    write_output(map, violations)

if __name__ == "__main__":
    main()