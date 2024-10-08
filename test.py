import numpy as np
from output_verifier import *
from bowl import write_output, light_bulbs
import copy
from test import *
import random
import math
from graphCreation import *
from printer import *
from betterGreedy import *
import sys

# Assuming sys.argv[1] is the input file, provide a default value for testing
#sys.argv = ['script.py', 'input_file.txt']

def get_nums(nummap):
    nums_list = []
    for i in range(len(nummap)):
        for j in range(len(nummap[0])):
            if nummap[i][j]:
                nums_list.append(nummap[i][j])

    sorted_nums_list = sorted(nums_list, key=lambda x: x.num, reverse=True)
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
                important.append((i, j))
            else:
                notimportant.append((i, j))
    random.shuffle(notimportant)
    random.shuffle(important)
    return notimportant + important

def count_lights(light_map):
    """Returns a list of all coordinates with lights in the light_map."""
    lights = [(i, j) for i in range(len(light_map)) for j in range(len(light_map[0])) if light_map[i][j]]
    return lights

def remove_random_lights(light_map, num_remove=5):
    """Randomly removes a specified number of lights from the light_map."""
    lights = count_lights(light_map)
    if len(lights) < num_remove:
        return light_map  # Not enough lights to remove
    
    lights_to_remove = random.sample(lights, num_remove)
    
    for (i, j) in lights_to_remove:
        light_map[i][j] = None  # Remove light
    
    return light_map

def evaluate_violations(map, lightmap):
    """Evaluate and return the number of violations."""
    return determine_violations(map)

def acceptance_probability(current_violations, new_violations, temperature):
    """Calculate the acceptance probability."""
    if new_violations < current_violations:
        return 1.0
    return math.exp((current_violations - new_violations) / temperature)

def simulated_annealing(map, lightmap, initial_temp=1000, cooling_rate=0.95, stopping_temp=1):
    """Performs simulated annealing to minimize the number of violations."""
    current_map = copy.deepcopy(map)
    current_lightmap = copy.deepcopy(lightmap)
    current_violations = evaluate_violations(current_map, current_lightmap)

    temp = initial_temp
    while temp > stopping_temp:
        # Create a new neighboring state by removing 5 lights
        new_lightmap = remove_random_lights(copy.deepcopy(current_lightmap), num_remove=5)
        
        # Update the map with the new light positions
        validate_board(current_map, get_locations(new_lightmap))
        
        # Calculate the number of violations for the new state
        new_violations = evaluate_violations(current_map, new_lightmap)

        # Determine if we should accept the new state
        if acceptance_probability(current_violations, new_violations, temp) > random.random():
            current_lightmap = new_lightmap
            current_violations = new_violations

        # Decrease the temperature
        temp *= cooling_rate
        print(f"Temperature: {temp:.2f}, Current Violations: {current_violations}")

    return current_map, current_lightmap, current_violations

def main():
    # Get initial state
    _, retMap = get_input_data(sys.argv[1])  # read input
    lightmap = [[None for _ in range(len(retMap[0]))] for _ in range(len(retMap))]
    nummap = [[None for _ in range(len(retMap[0]))] for _ in range(len(retMap))]
    map = find_important_squares(retMap, lightmap, nummap)
    find_collisions(retMap, map, nummap, lightmap)

    # Get sorted list of nums
    num_list = get_nums(nummap)
    simple_greedy(num_list)

    update_map(lightmap, map)
    violations = determine_violations(map)
    print(f"Initial violations before annealing: {violations}")

    # Run simulated annealing 100 times and track the best solution
    best_map = None
    best_lightmap = None
    best_violations = float('inf')  # Start with the worst possible score

    for run in range(100):
        print(f"\n--- Run {run + 1} ---")
        # Perform simulated annealing to minimize violations
        final_map, final_lightmap, final_violations = simulated_annealing(map, lightmap)
        
        # Update the best solution if the current run is better
        if final_violations < best_violations:
            best_violations = final_violations
            best_map = final_map
            best_lightmap = final_lightmap

        print(f"Run {run + 1} violations: {final_violations}")

    # Print and write the best result
    print(f"\nBest violations after 100 runs: {best_violations}")
    write_output(best_map, best_violations)

if __name__ == "__main__":
    main()
