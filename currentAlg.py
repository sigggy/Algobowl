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


def generate_neighbor(grid, poss_good_lights, poss_bad_lights, badLights, goodLights, num_bad_pops, num_good_pops):
    new_grid = copy.deepcopy(grid)

    new_bad_lights = copy.deepcopy(badLights)
    new_good_lights = copy.deepcopy(goodLights)

    for _ in range(num_bad_pops):
        light_pop = random.choice(new_bad_lights)
        new_grid[light_pop[0]][light_pop[1]] = '.'
        new_bad_lights.remove(light_pop)
    for _ in range(num_good_pops):
        light_pop = random.choice(new_good_lights)
        new_grid[light_pop[0]][light_pop[1]] = '.'
        new_good_lights.remove(light_pop)

    validate_board(new_grid, (poss_good_lights, poss_bad_lights), goodLights, badLights)

    return badLights, goodLights, new_grid, len(badLights)



def simulated_annealing(poss_good_lights, poss_bad_lights, badLights, goodLights, grid, T_initial, T_final, alpha):    
    best = grid
    best_eval = len(badLights)
    current, current_eval, current_bad_lights, current_good_lights = best, best_eval, badLights, goodLights
    T = T_initial
    scores = [best_eval]

    for i in range(100):
        t = T_initial / alpha 

        candidate_bad_lights, candidate_good_lights, candidate, candidate_eval = generate_neighbor(current, poss_good_lights, poss_bad_lights, current_bad_lights, current_good_lights, 10, 10)
        scores.append(candidate_eval)
        if candidate_eval < best_eval or random.random() < math.exp((current_eval - candidate_eval) / t):
            current, current_eval, current_bad_lights, current_good_lights = candidate, candidate_eval, candidate_bad_lights, candidate_good_lights
            if candidate_eval < best_eval:
                best, best_eval = candidate, candidate_eval
                scores.append(best_eval)

        if i % 10 == 0:
            print(f"Iteration {i}, Temperature {t:.3f}, Best Evaluation {best_eval:.5f}")

    return best, scores


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

        violations = determine_violations(map)
        violations_list.append(violations)

        if violations < best_violations:
            best_violations = violations
            best_map = copy.deepcopy(map)  
            best_light_map = copy.deepcopy(lightmap)  
    
    T_initial = np.std(violations_list)
    #T_initial = 200

    poss_good_lights, poss_bad_lights = get_locations(best_light_map)

    goodLights, badLights = validate_board(best_map, get_locations(best_light_map), [], []) 

    before_violations = determine_violations(best_map)

    output_map, scores = simulated_annealing(poss_good_lights, poss_bad_lights, badLights, goodLights, best_map, T_initial, T_final=0.5, alpha=0.95)

    print(f' violations before anneal {before_violations}')
    output_violations = determine_violations(output_map)
    print(f' violations after anneal {output_violations}')
    print(scores)
    write_output(output_map, output_violations)

if __name__ == "__main__":
    main()