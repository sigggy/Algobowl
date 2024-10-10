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

# Define add and remove bulb operations
# Define operations for adding, removing, and moving bulbs
def add_random_bulb(grid):
    """Randomly adds a light bulb 'L' to an empty position '.' in the grid."""
    empty_positions = [(i, j) for i in range(len(grid)) for j in range(len(grid[i])) if grid[i][j] == "."]
    if empty_positions:
        i, j = random.choice(empty_positions)
        grid[i][j] = "L"
    return grid

def remove_random_bulb(grid):
    """Randomly removes a light bulb 'L' from a position in the grid."""
    light_positions = [(i, j) for i in range(len(grid)) for j in range(len(grid[i])) if grid[i][j] == "L"]
    if light_positions:
        i, j = random.choice(light_positions)
        grid[i][j] = "."
    return grid

def move_random_bulb(grid):
    """Randomly moves a light bulb 'L' from one position to another empty position '.' in the grid."""
    light_positions = [(i, j) for i in range(len(grid)) for j in range(len(grid[i])) if grid[i][j] == "L"]
    empty_positions = [(i, j) for i in range(len(grid)) for j in range(len(grid[i])) if grid[i][j] == "."]
    if light_positions and empty_positions:
        # Remove a bulb from a random position
        i, j = random.choice(light_positions)
        grid[i][j] = "."
        # Add the bulb to a random empty position
        i, j = random.choice(empty_positions)
        grid[i][j] = "L"
    return grid

def count_violations(grid):
    """Placeholder function for counting the number of violations in the grid."""
    # Replace this with your actual logic to determine the number of violations in the board state.
    return random.randint(0, 10)

# Hill climbing function
def hill_climb(grid):
    """Hill climb to find a better solution by adding, removing, or moving bulbs."""
    current_eval = count_violations(grid)

    # Generate neighbors by performing small perturbations (add, remove, or move bulb)
    add_grid = add_random_bulb(copy.deepcopy(grid))
    remove_grid = remove_random_bulb(copy.deepcopy(grid))
    move_grid = move_random_bulb(copy.deepcopy(grid))

    # Evaluate the neighbors
    add_eval = count_violations(add_grid)
    remove_eval = count_violations(remove_grid)
    move_eval = count_violations(move_grid)

    # Select the best neighbor based on the number of violations
    best_eval = current_eval
    best_grid = grid

    if add_eval < best_eval:
        best_eval = add_eval
        best_grid = add_grid

    if remove_eval < best_eval:
        best_eval = remove_eval
        best_grid = remove_grid

    if move_eval < best_eval:
        best_eval = move_eval
        best_grid = move_grid

    # Return the best grid found and its evaluation
    return best_grid, best_eval

# Modified simulated annealing with hill climbing option
def simulated_annealing(grid, T_initial, T_final, alpha, use_hill_climb=False):    
    best = copy.deepcopy(grid)
    best_eval = count_violations(grid)
    current, current_eval = copy.deepcopy(grid), best_eval
    T = T_initial
    scores = [best_eval]

    # Define a safe range for the exponent to prevent overflow
    EXPONENT_CLAMP = 709  # Max value for math.exp to prevent overflow in Python

    for i in range(3000):  # Set a reasonable number of iterations
        t = max(T_initial * (alpha ** i), 1e-8)  # Avoid overflow issues and zero division

        # Use hill climbing to get the next candidate if specified, otherwise generate a random neighbor
        if use_hill_climb:
            candidate, candidate_eval = hill_climb(current)
        else:
            operation = random.choice([add_random_bulb, remove_random_bulb, move_random_bulb])
            candidate = operation(copy.deepcopy(current))
            candidate_eval = count_violations(candidate)

        # Accept the new solution if it’s better or based on probability if not
        try:
            acceptance_prob = math.exp((current_eval - candidate_eval) / t)
        except OverflowError:
            acceptance_prob = 0  # Handle overflow gracefully

        if candidate_eval < best_eval or random.random() < acceptance_prob:
            current, current_eval = candidate, candidate_eval
            if candidate_eval < best_eval:
                best, best_eval = candidate, candidate_eval
                scores.append(best_eval)

        if i % 10 == 0:
            print(f"Iteration {i}, Temperature {t:.3f}, Best Evaluation {best_eval:.5f}")

    return best, best_eval, scores


   


import random

def get_nums(nummap):
    nums_list = []
    for i in range(len(nummap)):
        for j in range(len(nummap[0])):
            if nummap[i][j]:
                nums_list.append(nummap[i][j])

    # Add a small random noise to the `num` attribute to introduce randomness
    random_noise_factor = .1  # Adjust this factor to control randomness level
    nums_list_with_noise = [(num, num.num + random.uniform(-random_noise_factor, random_noise_factor)) for num in nums_list]

    # Sort nums_list by the noisy value in descending order
    sorted_nums_list = [num for num, _ in sorted(nums_list_with_noise, key=lambda x: x[1], reverse=True)]

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
    #T_initial = 200
    output_map, output_violations, scores = simulated_annealing(best_map, T_initial, T_final=1, alpha=0.95)
    lightmap = [[None for _ in range(len(retMap[0]))] for _ in range(len(retMap))]
    update_light_map(output_map, lightmap)
    validate_board(output_map, get_locations(lightmap))
    output_violations = determine_violations(output_map)
    print(f' violations before anneal {before_violations}')
    print(f' violations after anneal {output_violations}')
    print(scores)
    write_output(output_map, output_violations)


if __name__ == "__main__":
    main()