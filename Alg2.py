import numpy as np
import random
import copy
from output_verifier import *
from bowl import write_output, light_bulbs
from test import *
from graphCreation import *
from printer import *
from betterGreedy import *

def remove_random_Ls(grid, num_to_remove=1):
    """Remove a fixed number of lights from the grid."""
    positions = [(i, j) for i in range(len(grid)) for j in range(len(grid[i])) if grid[i][j] == "L"]
    if len(positions) < num_to_remove:
        num_to_remove = len(positions)
    positions_to_remove = random.sample(positions, num_to_remove)
    for i, j in positions_to_remove:
        grid[i][j] = "."
    return grid

def add_random_L(grid, num_to_add=1):
    """Add a fixed number of lights at random positions in the grid."""
    empty_positions = [(i, j) for i in range(len(grid)) for j in range(len(grid[i])) if grid[i][j] == "."]
    if len(empty_positions) < num_to_add:
        num_to_add = len(empty_positions)
    positions_to_add = random.sample(empty_positions, num_to_add)
    for i, j in positions_to_add:
        grid[i][j] = "L"
    return grid

def generate_neighbor(retMap):
    """Generate a neighboring state by removing and adding a light."""
    # Copy the current state to create a neighbor
    retMap_copy = copy.deepcopy(retMap)

    # Remove and add a light at random
    retMap_copy = remove_random_Ls(retMap_copy, num_to_remove=1)
    retMap_copy = add_random_L(retMap_copy, num_to_add=1)

    # Recalculate the configuration
    lightmap = [[None for _ in range(len(retMap_copy[0]))] for _ in range(len(retMap_copy))]
    nummap = [[None for _ in range(len(retMap_copy[0]))] for _ in range(len(retMap_copy))]
    map = find_important_squares(retMap_copy, lightmap, nummap)
    find_collisions(retMap_copy, map, nummap, lightmap)
    num_list = get_nums(nummap)  # Get sorted list of nums
    simple_greedy(num_list)
    update_map(lightmap, map)
    validate_board(map, get_locations(lightmap))
    return map

def simulated_annealing(init_grid, T_initial, T_final, alpha):
    """Perform the simulated annealing optimization."""
    current_state = copy.deepcopy(init_grid)
    current_energy = determine_violations(current_state)

    # Initialize best state and energy
    best_state = copy.deepcopy(current_state)
    best_energy = current_energy

    # Track energy levels for debugging
    energies = [current_energy]
    T = T_initial

    while T > T_final:
        for _ in range(100):  # Number of iterations at each temperature step
            neighbor = generate_neighbor(current_state)
            neighbor_energy = determine_violations(neighbor)
            delta_energy = neighbor_energy - current_energy

            # Calculate acceptance probability
            acceptance_probability = np.exp(-delta_energy / T)

            # Always accept better solutions, otherwise accept based on probability
            if delta_energy < 0 or random.random() < acceptance_probability:
                current_state = neighbor
                current_energy = neighbor_energy

                # Track the best state found
                if current_energy < best_energy:
                    best_state = copy.deepcopy(current_state)
                    best_energy = current_energy

            energies.append(current_energy)

        # Reduce temperature using a cooling schedule
        T *= alpha

        print(f"Temperature: {T:.2f}, Current Energy: {current_energy}, Best Energy: {best_energy}")

    print(f"Minimum energy achieved: {np.min(energies)}")
    return best_state

# Remaining functions such as get_nums, simple_greedy, get_locations, and main stay the same.

if __name__ == "__main__":
    main()
